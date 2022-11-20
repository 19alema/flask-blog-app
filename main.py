from flask import Flask, flash,request, jsonify,url_for,render_template,redirect, Blueprint
from flask_login import current_user
from datetime import datetime
from models import Posts, Comments, Authors, Profiles
from flask_login import login_required


main = Blueprint("main", __name__,)

@main.route("/", methods=['GET'])
def index():
    return render_template("pages/index.html")


@main.route("/posts", methods=['GET', 'POST'])
@login_required
def posts():
    if request.method=='GET':
        return render_template("pages/create_blog.html")
    else:
        title = request.form.get('title');
        body = request.form.get("body");
        
        status = True if request.form.get("status") else False;
        author = current_user.id;

        new_Post = Posts(title=title,body=body,status=status,author=author)

        new_Post.insert()
        
        return redirect(url_for('main.blogs'))

@main.route("/blogs")
def blogs():
    blogs_container=[]
    blogs = Posts.query.all()

    for blog in blogs:

        author = Profiles.query.filter(Profiles.author_id==blog.author).one_or_none()

        blogs_container.append({
            "id": blog.id,
            "author": f'{author.first_name} {author.last_name}',
            "title": blog.title,
            "status":blog.status,
        })
    return render_template('pages/blogs.html', blogs_data=blogs_container)


@main.route("/bloggers/<int:author_id>/profile", methods=['GET','POST'])
@login_required
def profile(author_id):

    author_profile=[]
    authors = Authors.query.filter(Authors.id == author_id).one_or_none();
    profiles = Profiles.query.filter(Profiles.author_id==author_id).one_or_none();
    blogs = Posts.query.filter(Posts.author == author_id).all()
    author_profile.append({
        'id': authors.id,
        'email':authors.email,
        'username': authors.username,
        'last_name':profiles.last_name,
        'first_name':profiles.first_name,
        'bio':profiles.bio,
        'blogs': blogs,
        'total':len(blogs)
    })

    

    return render_template("pages/profile.html", author_data=author_profile)


@main.route("/authors")
def bloggers():
    bloggers =[]
    authors = Authors.query.all();

    for author in authors:
      
        profile = Profiles.query.filter(Profiles.author_id==author.id).one_or_none();
        author ={
            'id': author.id,
            'username': author.username,
            'name': f'{profile.first_name} {profile.last_name} '
        }
    
        bloggers.append(author)

    return render_template("pages/bloggers.html", author=bloggers)

@main.route("/blogger", methods=['GET', 'POST'])
@login_required
def blogger():
    if request.method == 'GET':
        return render_template("pages/create_profile.html")
    else:
        first_name = request.form.get("first_name")
        last_name = request.form.get("last_name")
        bio = request.form.get("bio")
        author_id = current_user.id

        author_profile = Profiles(first_name=first_name,last_name=last_name,bio=bio, author_id=author_id)
     
        flash("Profile Created at Success")
        author_profile.insert()

    return redirect(url_for("main.blog"))


@main.route("/blog")
def blog():
    id = current_user.id
    data =[]
    blogger = Authors.query.filter(Authors.id ==id).one_or_none()
    profile = Profiles.query.filter(Profiles.author_id ==id).one_or_none();
    return render_template("pages/blog.html",blogger=blogger)

@main.route("/bloggers/<int:blogger_id>/blog", methods=['GET', 'POST'])
def create_blog(blogger_id):
    if request.method =='GET':
        return render_template("pages/create_blog.html")


# SINGLE BLOG and BLOG comments
@main.route("/blogs/blog/<int:blog_id>", methods=['GET', 'POST'])
@login_required
def blog_detail(blog_id):
    if request.method=='GET':
        post_comment =[]
        comment =[]
        comment_poster=[]
        the_blog = Posts.query.filter(Posts.id==blog_id).one_or_none()

        comments = Comments.query.all()

        commentor =Authors.query.filter(Authors.id ==blog_id).all()
        comment = Comments.query.filter(Comments.post_id == blog_id).all()
        total_posts = len(comment)

        for comm in comment:
            posters =  Posts.query.filter(Posts.id==comm.post_id).all();
            for post in posters:
                posters = Authors.query.filter(Authors.id==post.author).all()
                for poster in posters:
                    username = poster.username;
                    post_comment.append({
                            'comment': comm,
                            'commentor': username,
                        })
        return render_template("pages/single_blog.html",total=total_posts, blog=the_blog, comments=post_comment)
    else:
        posts= Posts.query.all()
    
        for post in posts:
            post_id = post.author
        post_comment = request.form.get("comment")
        new_comment =Comments(post_id=blog_id, post_comment=post_comment);
        new_comment.insert()

    return redirect(url_for("main.blog_detail", blog_id=blog_id))


# DELETE BLOG
@main.route('/blogs/<int:blog_id>/delete', methods=['DELETE','GET'])
def delete_blog(blog_id):
     
    delete_blog = Posts.query.filter(Posts.id == blog_id).one_or_none();
    print(delete_blog)
    if delete_blog.author ==current_user.id:
        delete_blog.delete()
    return redirect(url_for("main.profile", author_id=current_user.id))





        

        


