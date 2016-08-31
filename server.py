from flask import *
from models import *


app = Flask('User Story Manager')


@app.before_first_request
def connect_db():
    db.connect()
    db.drop_tables(Story, safe=True)
    db.create_table(Story, safe=True)
    Story.create(
        story_title='Test',
        user_story='Testing the database',
        acceptance_criteria='If I see this story, it is good :D',
        business_value=99999,
        estimation=99999
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
    return render_template('list.html', stories=story_list)


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
    return render_template('form.html', data=[filling_values])


@app.route('/story', methods=['POST'])
def create_story():
    filling_values = {
        'Fill': True,
        'title': 'Add Story',
        'header': 'User Story Manager  - Add new Story',
        'submit': 'Create',
        'message': 'Invalid data,please try again!',
        'story': 'create_story',
        'url': '/save_story'}
    story = Story.create(
        story_title=request.form['title'],
        user_story=request.form['userstory'],
        acceptance_criteria=request.form['acccrit'],
        business_value=request.form['bisval'],
        estimation=request.form['estimation'],
        status=request.form['status']
    )
    if story.check_if_valid():
        story.save()
        return redirect('/list')
    else:
        return render_template('form.html', data=[filling_values])


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

    return render_template('form.html', data=[filling_values, story])


@app.route('/story/<story_id>', methods=['POST'])
def edit_story(story_id):
    story = Story.select().where(Story.story_id == story_id).get()
    story.story_title = request.form['title']
    story.user_story = request.form['userstory']
    story.acceptance_criteria = request.form['acccrit']
    story.business_value = request.form['bisval']
    story.estimation = request.form['estimation']
    story.status = request.form['status']
    if story.check_if_valid():
        story.save()
    return redirect(url_for('list_stories'))


@app.route('/delete/<story_id>', methods=['POST'])
def delete_story(story_id):
    story = Story.select().where(Story.story_id == story_id).get()
    story.delete_instance()
    story.save()
    print('volt valami csak szar')
    return redirect(url_for('list_stories'))


