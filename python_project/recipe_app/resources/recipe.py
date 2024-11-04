from flask_restful import Resource, reqparse
from models import Recipe, db
from flask_jwt_extended import jwt_required
from utils.decorators import role_required

recipe_parser = reqparse.RequestParser()
recipe_parser.add_argument('name', required=True)
recipe_parser.add_argument('ingredients', required=True)
recipe_parser.add_argument('steps', required=True)
recipe_parser.add_argument('prep_time', type=int, required=True)
recipe_parser.add_argument('difficulty', required=True)

class RecipeList(Resource):
    def get(self):
        recipes = Recipe.query.all()
        return [{'id': r.id, 'name': r.name, 'ingredients': r.ingredients, 'steps': r.steps, 'prep_time': r.prep_time, 'difficulty': r.difficulty} for r in recipes], 200

    @jwt_required()
    @role_required('admin')
    def post(self):
        data = recipe_parser.parse_args()
        new_recipe = Recipe(**data)
        db.session.add(new_recipe)
        db.session.commit()
        return {'message': 'Recipe created'}, 201

class RecipeResource(Resource):
    def get(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        return {'id': recipe.id, 'name': recipe.name, 'ingredients': recipe.ingredients, 'steps': recipe.steps, 'prep_time': recipe.prep_time, 'difficulty': recipe.difficulty}

    @jwt_required()
    @role_required('admin')
    def put(self, recipe_id):
        data = recipe_parser.parse_args()
        recipe = Recipe.query.get_or_404(recipe_id)
        recipe.name = data['name']
        recipe.ingredients = data['ingredients']
        recipe.steps = data['steps']
        recipe.prep_time = data['prep_time']
        recipe.difficulty = data['difficulty']
        db.session.commit()
        return {'message': 'Recipe updated'}, 200

    @jwt_required()
    @role_required('admin')
    def delete(self, recipe_id):
        recipe = Recipe.query.get_or_404(recipe_id)
        db.session.delete(recipe)
        db.session.commit()
        return {'message': 'Recipe deleted'}, 200
