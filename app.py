from flask import Flask, render_template, redirect, url_for, request, flash, session
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from forms import DocumentForm
from models import db, Document, Version

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///cloud_notebook.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db.init_app(app)

# Create database
@app.before_first_request
def create_tables():
    db.create_all()

# Document list and search
@app.route("/", methods=["GET", "POST"])
def home():
    query = request.args.get("query")
    if query:
        documents = Document.query.filter(Document.title.contains(query)).all()
    else:
        documents = Document.query.all()
    return render_template("home.html", documents=documents)

# Document creation and editing
@app.route("/document/new", methods=["GET", "POST"])
@app.route("/document/<int:doc_id>", methods=["GET", "POST"])
def document(doc_id=None):
    form = DocumentForm()
    document = Document.query.get(doc_id) if doc_id else None

    if form.validate_on_submit():
        if document:
            document.title = form.title.data
            document.content = form.content.data
            db.session.commit()
            flash("Document updated.")
        else:
            new_document = Document(title=form.title.data, content=form.content.data)
            db.session.add(new_document)
            db.session.commit()
            flash("Document created.")
        return redirect(url_for("home"))

    return render_template("document.html", form=form, document=document)

# Version control
@app.route("/document/<int:doc_id>/versions")
def versions(doc_id):
    document = Document.query.get(doc_id)
    return render_template("versions.html", document=document)

# Version restore
@app.route("/document/<int:doc_id>/restore/<int:version_id>")
def restore_version(doc_id, version_id):
    version = Version.query.get(version_id)
    document = Document.query.get(doc_id)
    document.content = version.content
    db.session.commit()
    flash("Version restored.")
    return redirect(url_for("document", doc_id=doc_id))

# Run the app
if __name__ == "__main__":
    app.run(debug=True)
