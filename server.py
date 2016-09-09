from flask import *
from models import *


app = Flask('User Story Manager')


@app.before_first_request
def connect_db():
    db.connect()
    db.drop_table(Story, fail_silently=True)
    db.create_table(Story, safe=True)
    Story.create(
        story_title='Test1',
        user_story='Testing the database312',
        acceptance_criteria='If I see this story, it is good :D',
        business_value=200,
        estimation=3
    )
    Story.create(
        story_title='Test2',
        user_story='Testing the databa123se',
        acceptance_criteria='If I see this321 story, it is good :D',
        business_value=100,
        estimation=4
    )
    Story.create(
        story_title='Test3',
        user_story='Testing the database',
        acceptance_criteria='If I see thi3123s story, it is good :D',
        business_value=300,
        estimation=5
    )


# @app.after_request
# def close_db(**kwargs):
#     db.close()
@app.route('/list')
@app.route('/')
def list_stories():
    story_list = []
    stories = Story.select()
    for story in stories:
        story_list.append(story)
    data = [{
        'title': 'Story List',
        }]
    return render_template('bootstrap_list.html', data=data, stories=story_list)


@app.route('/story', methods=['GET'])
def fill_forms():
    filling_values = {
        'fill': True,
        'title': 'Add Story',
        'header': 'User Story Manager  - Add new Story',
        'submit': 'Save',
        'message': '',
        'story': 'create_story',
        'url': '/story'
    }
    return render_template('bootstrap_form.html', data=[filling_values])


@app.route('/story', methods=['POST'])
def create_story():
    story = Story.create(
        story_title=request.form['title'],
        user_story=request.form['userstory'],
        acceptance_criteria=request.form['acccrit'],
        business_value=request.form['bisval'],
        estimation=request.form['estimation'],
        status=request.form['status']
    )
    story.save()
    return redirect('/list')


@app.route('/story/<story_id>')
def show_by_id(story_id):
    story = Story.select().where(Story.story_id == story_id).get()
    filling_values = {
        'fill': False,
        'title': 'Edit Story',
        'header': 'User Story Manager  - Edit Story',
        'submit': 'Save',
        'story': 'edit_story',
        'url': '/story/' + str(story.story_id)
    }

    return render_template('bootstrap_form.html', data=[filling_values, story])


@app.route('/story/<story_id>', methods=['POST'])
def edit_story(story_id):
    story = Story.select().where(Story.story_id == story_id).get()
    story.story_title = request.form['title']
    story.user_story = request.form['userstory']
    story.acceptance_criteria = request.form['acccrit']
    story.business_value = request.form['bisval']
    story.estimation = request.form['estimation']
    story.status = request.form['status']
    story.save()
    return redirect(url_for('list_stories'))


@app.route('/delete/<story_id>', methods=['POST', 'GET'])
def delete_story(story_id):
    story = Story.select().where(Story.story_id == story_id).get()
    story.delete_instance()
    story.save()
    return redirect(url_for('list_stories'))


