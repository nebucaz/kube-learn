import os
from flask import Flask
from flask_restx import Api, Resource, fields
from example.worker import fetch_task

app = Flask(__name__)
app.config['CELERY_BROKER_URL'] = os.getenv('CELERY_BROKER_URL')
app.config['CELERY_RESULT_BACKEND'] = os.getenv('CELERY_RESULT_BACKEND')

api = Api(app, version='1.0', title='Example API', description='Example API')
ns = api.namespace('example')
api.add_namespace(ns)

task_model = ns.model('Task', {
    'url': fields.String(required=True,
                          description='The url to process')
})


@ns.route('/fetch', methods=['POST'])
class FetchTask(Resource):
    @ns.expect(task_model)
    @ns.response(202, 'Fetch task accepted')
    def post(self):
        task = fetch_task.apply_async((ns.payload.get('url'),))
        return {'taskId': task.id}, 202

@ns.route('/status/<string:task_id>', methods=['GET'])
class TaskStatus(Resource):
    #ns.expect(parser)
    @ns.response(200, 'Success')
    def get(self, task_id):
        #args = parser.parse_args()
        task = fetch_task.AsyncResult(task_id)
        return {
            'taskId': task_id,
            'state': task.state,
            'result': task.result
        }





if __name__ == '__main__':
    app.run(port=5001, host='0.0.0.0')