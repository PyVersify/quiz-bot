import discord
from src.utils import QuizFileHandler

class QuizSelectView(discord.ui.View):
    """A view for selecting a quiz.
    
    Attributes:
        quizzes (list): The list of quizzes.
        select (discord.ui.Select): The select menu for choosing a quiz.
    
    Methods:
        quiz_callback: The callback function for the select menu.
    """

    def __init__(self) -> None:
        super().__init__()

        with QuizFileHandler('data/dir.json') as file:
            data = file.load()
            self.quizzes = data['quizzes']
        
        self.select = discord.ui.Select(
            placeholder='Select a Quiz', 
            options=[
                discord.SelectOption(
                    label=quiz['title'], 
                    value=quiz['id'],
                    description=quiz['description']
                ) for quiz in self.quizzes
            ]
        )
        
        self.select.callback = self.quiz_callback
        self.add_item(self.select)
    
    async def quiz_callback(self, interaction: discord.Interaction) -> None:
        quiz_id = self.select.values[0]
        quiz_view = QuizView(quiz_id)
        await interaction.response.edit_message(
            content=f"Starting quiz: {quiz_id}",
            view=quiz_view
        )


class QuizView(discord.ui.View):
    """A view for displaying multiple choice quiz questions.
    
    Attributes:
        quiz_data (dict): The quiz data.
        current_question (int): The current question number.
        score (int): The current score.
        buttons (list): The multiple choice buttons.
    
    Methods:
        create_buttons: Creates the multiple choice buttons for the current question.
        make_callback: Create a callback function for the button.
        check_answer: Check if the selected answer is correct.
        show_questions: Display the current question with updated embed.
        end_quiz: End the quiz and display the final score.
    """

    quiz_data: dict
    current_question: int
    score: int
    buttons: list

    def __init__(self, quiz_id: str) -> None:
        super().__init__()
        
        self.current_question = 0
        self.score = 0
        
        with QuizFileHandler(f'data/quiz/{quiz_id}.json') as file:
            self.quiz_data = file.load()
        
        self.buttons = []
    
    def create_buttons(self) -> None:
        """Creates the multiple choice buttons for the current question.
        
        Returns:
            None
        """
        self.clear_items()
        self.buttons = []

        current_q = self.quiz_data['quiz'][self.current_question]

        for letter, choice in current_q['options'].items():
            label = f"{letter}. {choice[:72]}" if len(choice) > 72 else f"{letter}. {choice}"

            button = discord.ui.Button(
                label=label,
                style=discord.ButtonStyle.primary,
                custom_id=letter
            )

            button.callback = self.make_callback(letter)
            self.buttons.append(button)
            self.add_item(button)
    
    def make_callback(self, letter: str) -> callable:
        """Create a callback function for the button.
        
        Args:
            letter (str): The letter of the answer.
        
        Returns:
            callable: The callback function.
        """
        async def button_callback(interaction: discord.Interaction) -> None:
            """The callback function for the button.
            
            Args:
                interaction (discord.Interaction): The interaction object.
                
            Returns:
                None
            """
            await self.check_answer(interaction, letter)
        
        return button_callback
    
    async def check_answer(self, interaction: discord.Interaction, choice: str) -> None:
        """Check if the selected answer is correct.
        
        Args:
            interaction (discord.Interaction): The interaction object.
            choice (str): The selected answer.
        
        Returns:
            None
        """
        correct = self.quiz_data['quiz'][self.current_question]['answer']
        if choice == correct:
            self.score += 1
            await interaction.response.send_message(
                "Correct! ✅", 
                ephemeral=True
            )
        else:
            await interaction.response.send_message(
                f"Incorrect! ❌ The correct answer was {correct}.", 
                ephemeral=True
            )
        self.current_question += 1
        if self.current_question < len(self.quiz_data['quiz']):
            await self.show_questions(interaction)
        else:
            await self.end_quiz(interaction)

    
    async def show_questions(self, interaction: discord.Interaction) -> None:
        """Display the current question with updated embed.
        
        Args:
            interaction (discord.Interaction): The interaction object.
        
        Returns:
            None
        """
        current_q = self.quiz_data['quiz'][self.current_question]
        embed = discord.Embed(
            title=f"Question {self.current_question + 1}/{len(self.quiz_data['quiz'])}",
            description=current_q['question'],
            color=discord.Color.blurple()
        )

        embed.set_footer(text=f"Score: {self.score}/{self.current_question}")

        self.create_buttons()

        await interaction.message.edit(embed=embed, view=self)

    async def end_quiz(self, interaction: discord.Interaction) -> None:
        """End the quiz and display the final score.
        
        Args:
            interaction (discord.Interaction): The interaction object.
        
        Returns:
            None
        """
        # Clear all buttons
        self.clear_items()

        embed = discord.Embed(
            title="Quiz Complete! 🎉",
            description=f"Final score: {self.score}/{len(self.quiz_data['quiz'])}",
            color=discord.Color.green()
        )

        percentage = (self.score / len(self.quiz_data['quiz'])) * 100
        embed.add_field(
            name="Performance",
            value=f"You scored {percentage:.2f}%!",
            inline=False
        )

        return_button = discord.ui.Button(
            label="Return",
            style=discord.ButtonStyle.success,
            custom_id="return_button"
        )

        async def return_callback(interaction: discord.Interaction) -> None:
            view = QuizSelectView()
            await interaction.response.edit_message(
                content="Select a quiz:",
                embed=None,
                view=view
            )
        
        return_button.callback = return_callback
        self.add_item(return_button)

        await interaction.message.edit(embed=embed, view=self)