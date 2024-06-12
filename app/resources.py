from flask_restx import Resource , Namespace

from .api_models import course_model , student_model , course_inputs , students_inputs

from .models import Course , Student

from .extensions import db

ns = Namespace("api")

@ns.route("/hello")
class Hello(Resource):
    def get(self):
        return {"hello" : "restx"}
    
@ns.route("/courses")
class Course_LIST_API(Resource):
    @ns.marshal_list_with(course_model)
    def get(self):
        return Course.query.all()
    
    @ns.expect(course_inputs)
    @ns.marshal_with(course_model)
    def post(self):
        # print(ns.payload)
        course =  Course(name=ns.payload["name"])
        db.session.add(course)
        db.session.commit()
        return course , 201
    
@ns.route("/course/<int:id>")
class CourseAPI(Resource):
    @ns.marshal_with(course_model)
    def get(self , id):
        course = Course.query.get(id)
        return course
    
    @ns.expect(course_inputs)
    @ns.marshal_with(course_model)
    def put(self, id):
        course = Course.query.get(id)
        course.name = ns.payload["name"]
        db.session.commit()
        return course

    def delete(self, id):
        course = Course.query.get(id)
        db.session.delete(course)
        db.session.commit()
        return {"message" : "Course with {id} has been deleted successfully."} , 204


@ns.route("/students")
class StudentAPI(Resource):
    @ns.marshal_list_with(student_model)
    def get(self):
        return Student.query.all()
    
    @ns.expect(students_inputs)
    @ns.marshal_with(student_model)
    def post(self):
        # print(ns.payload)
        student =  Student(name=ns.payload["name"], course_id = ns.payload["course_id"])
        db.session.add(student)
        db.session.commit()
        return student , 201
    
@ns.route("/student/<int:id>")
class StudentAPI(Resource):
    @ns.marshal_with(student_model)
    def get(self , id):
        student =  Student.query.get(id)
        return student
    
    @ns.expect(students_inputs)
    @ns.marshal_with(student_model)
    def put(self, id):
        student = Student.query.get(id)
        student.name = ns.payload["name"]
        student.course_id = ns.payload["course_id"]
        db.session.commit()
        return student


    # @ns.expect(students_inputs)
    # @ns.marshal_with(student_model)
    def delete(self, id):
        student = Student.query.get(id)
        db.session.delete(student)
        db.session.commit()
        return {"message" : "Student with {id} has been deleted successfully."} , 204
