from flask import Flask, request, render_template, redirect, flash, session
from flask_debugtoolbar import DebugToolbarExtension
from surveys import surveys, satisfaction_survey

RESPONSES_KEY = 'responses'

app = Flask(__name__)
app.config['SECRET_KEY'] = "scamp"

debug = DebugToolbarExtension(app)




@app.route('/')
def show_survey():
    """Start the survey"""
    title = satisfaction_survey.title
    instructions = satisfaction_survey.instructions

    return render_template('base.html', title=title, instructions=instructions)


@app.route('/begin', methods=['POST'])
def begin():

    session[RESPONSES_KEY] = []
    return redirect('/questions/0')


@app.route('/questions/<int:num>')
def show_question(num):
    """Show current question""" 
    questions = satisfaction_survey.questions
    responses = session.get(RESPONSES_KEY)

    if (responses is None):
        #Trying to access questions too soon
        return redirect('/')
    
    if (len(responses) == len(questions)):
        #Survey is complete, redirect and thank them
        return redirect('/results')
    
    if(len(responses) != num):
        #Trying to go out of order
        return redirect(f'/questions/{len(responses)}')
      
    question = questions[num].question
    choices = questions[num].choices
   
    return render_template('questions.html', question=question, num=num, choices=choices)



@app.route('/question', methods=['POST'])
def new_question():
    """Get the answer from the question and redirect to new question"""
    choice = request.form.get('choice')
    responses = session[RESPONSES_KEY]

    if (choice is None):
        #Trying to move on without answering
        flash("Please select and answer before continuing")     
    else:
        #Save answer to responses list
        responses.append(choice)
        session[RESPONSES_KEY] = responses

    return redirect(f'/questions/{len(responses)}')


@app.route('/results')
def complete():
    """Show thank you page and that survey is complete"""
    
    return render_template('results.html')