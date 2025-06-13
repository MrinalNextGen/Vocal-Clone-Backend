import logging
from flask import Blueprint, request, jsonify
from models import Blog
from database import db
from datetime import datetime

logger = logging.getLogger(__name__)
blog_routes = Blueprint('blog_routes', __name__)

@blog_routes.route('/health', methods=['GET'])
def health_check():
    logger.info("Health check requested")
    try:
        db.session.execute('SELECT 1')
        return jsonify({
            "success": True, 
            "message": "API is healthy", 
            "status": "success",
            "database": "connected"
        })
    except Exception as e:
        logger.error(f"Health check failed: {str(e)}")
        return jsonify({
            "success": False,
            "message": "Database connection failed",
            "error": str(e)
        }), 500

@blog_routes.route('/blogs', methods=['GET'])
def get_all_blogs():
    try:
        logger.info("GET /api/blogs - Fetching all blogs from database")
        blogs = Blog.query.order_by(Blog.createdAt.desc()).all()
        logger.info(f"GET /api/blogs - Successfully fetched {len(blogs)} blogs from database")
        return jsonify({"success": True, "data": [blog.to_dict() for blog in blogs]})
    except Exception as e:
        logger.error(f"GET /api/blogs - Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500

@blog_routes.route('/blogs', methods=['POST'])
def create_blog():
    try:
        logger.info("POST /api/blogs - Creating new blog in database")
        data = request.get_json()
        logger.info(f"POST /api/blogs - Received data: {data}")
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        if not data.get('heading') or not data.get('description'):
            return jsonify({
                "success": False,
                "error": "Heading and description are required"
            }), 400
        
        blog = Blog(
            image=data.get('image'),
            heading=data.get('heading'),
            subHeading=data.get('subHeading'),
            description=data.get('description'),
            author=data.get('author', 'Current User'),
            authorImage=data.get('authorImage'),
            isFavorite=data.get('isFavorite', False)
        )
        
        errors = blog.validate()
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        
        db.session.add(blog)
        db.session.commit()
        
        logger.info(f"POST /api/blogs - Successfully created blog with ID: {blog.id}")
        return jsonify({"success": True, "data": blog.to_dict()}), 201
        
    except Exception as e:
        logger.error(f"POST /api/blogs - Exception: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@blog_routes.route('/blogs/<int:blog_id>', methods=['PUT'])
def update_blog(blog_id):
    try:
        logger.info(f"PUT /api/blogs/{blog_id} - Updating blog in database")
        data = request.get_json()
        
        if not data:
            return jsonify({"success": False, "error": "No data provided"}), 400
        
        blog = Blog.query.get_or_404(blog_id)
        
        blog.image = data.get('image', blog.image)
        blog.heading = data.get('heading', blog.heading)
        blog.subHeading = data.get('subHeading', blog.subHeading)
        blog.description = data.get('description', blog.description)
        blog.author = data.get('author', blog.author)
        blog.authorImage = data.get('authorImage', blog.authorImage)
        blog.isFavorite = data.get('isFavorite', blog.isFavorite)
        blog.updatedAt = datetime.utcnow()
        
        errors = blog.validate()
        if errors:
            return jsonify({"success": False, "errors": errors}), 400
        
        db.session.commit()
        
        logger.info(f"PUT /api/blogs/{blog_id} - Successfully updated blog")
        return jsonify({"success": True, "data": blog.to_dict()})
        
    except Exception as e:
        logger.error(f"PUT /api/blogs/{blog_id} - Exception: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "error": str(e)}), 500

@blog_routes.route('/blogs/<int:blog_id>', methods=['DELETE'])
def delete_blog(blog_id):
    try:
        logger.info(f"DELETE /api/blogs/{blog_id} - Deleting blog from database")
        blog = Blog.query.get_or_404(blog_id)
        
        blog_data = blog.to_dict()
        db.session.delete(blog)
        db.session.commit()
        
        logger.info(f"DELETE /api/blogs/{blog_id} - Successfully deleted blog")
        return jsonify({"success": True, "data": blog_data})
        
    except Exception as e:
        logger.error(f"DELETE /api/blogs/{blog_id} - Error: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Blog not found"}), 404

@blog_routes.route('/blogs/<int:blog_id>/favorite', methods=['PATCH'])
def toggle_favorite(blog_id):
    try:
        logger.info(f"PATCH /api/blogs/{blog_id}/favorite - Toggling favorite")
        blog = Blog.query.get_or_404(blog_id)
        
        blog.isFavorite = not blog.isFavorite
        blog.updatedAt = datetime.utcnow()
        db.session.commit()
        
        logger.info(f"PATCH /api/blogs/{blog_id}/favorite - Successfully toggled favorite")
        return jsonify({"success": True, "data": blog.to_dict()})
        
    except Exception as e:
        logger.error(f"PATCH /api/blogs/{blog_id}/favorite - Error: {str(e)}")
        db.session.rollback()
        return jsonify({"success": False, "error": "Blog not found"}), 404

@blog_routes.route('/blogs/favorites', methods=['GET'])
def get_favorite_blogs():
    try:
        logger.info("GET /api/blogs/favorites - Fetching favorite blogs")
        favorite_blogs = Blog.query.filter_by(isFavorite=True).order_by(Blog.createdAt.desc()).all()
        
        return jsonify({
            "success": True, 
            "data": [blog.to_dict() for blog in favorite_blogs], 
            "count": len(favorite_blogs)
        })
    except Exception as e:
        logger.error(f"GET /api/blogs/favorites - Error: {str(e)}")
        return jsonify({"success": False, "error": str(e)}), 500
