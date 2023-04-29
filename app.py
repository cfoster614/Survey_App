from flask import Flask, request, render_template, redirect, flash
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, satisfaction_survey

app = Flask(__name__)
app.config['SECRET_KEY'] = "scamp"

debug = DebugToolbarExtension(app)


RESPONSES = []

@app.route('/')
def show_survey():
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions
    return render_template('base.html', title=title, instructions=instructions)


@app.route('/questions/<int:num>')
def show_questions(num): 
    questions = satisfaction_survey.questions
     
    if (RESPONSES is None):
        return redirect('/')
    
    if (len(RESPONSES) == len(questions)):
        return redirect('/results')
    
    if(len(RESPONSES) != num):
        return redirect(f'/questions/{len(RESPONSES)}')
      
    question = questions[num].question
    choices = questions[num].choices
   
    return render_template('questions.html', question=question, num=num, choices=choices)



@app.route('/question', methods=['POST'])
def new_question():
    choice = request.form.get('choice')

    if (choice is None):
        flash("Please select and answer before continuing")     
    else:
        RESPONSES.append(choice)

    return redirect(f'/questions/{len(RESPONSES)}')


@app.route('/results')
def complete():
    return render_template('results.html')