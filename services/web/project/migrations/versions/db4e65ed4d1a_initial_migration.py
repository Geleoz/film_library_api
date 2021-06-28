"""Initial migration.

Revision ID: db4e65ed4d1a
Revises: 
Create Date: 2021-07-05 12:55:10.908008

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = 'db4e65ed4d1a'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('director',
    sa.Column('director_id', sa.Integer(), nullable=False),
    sa.Column('first_name', sa.String(length=32), nullable=False),
    sa.Column('last_name', sa.String(length=32), nullable=False),
    sa.Column('birth_date', sa.Date(), nullable=True),
    sa.PrimaryKeyConstraint('director_id')
    )
    op.create_table('genre',
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.Column('name', sa.String(length=32), nullable=False),
    sa.PrimaryKeyConstraint('genre_id')
    )
    op.create_table('user',
    sa.Column('user_id', sa.Integer(), nullable=False),
    sa.Column('username', sa.String(length=32), nullable=False),
    sa.Column('email', sa.String(length=64), nullable=False),
    sa.Column('password', sa.String(length=64), nullable=False),
    sa.PrimaryKeyConstraint('user_id'),
    sa.UniqueConstraint('email'),
    sa.UniqueConstraint('username')
    )
    op.create_table('film',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('title', sa.String(length=64), nullable=False),
    sa.Column('release_date', sa.Date(), nullable=False),
    sa.Column('description', sa.Text(), nullable=True),
    sa.Column('rating', sa.Integer(), nullable=False),
    sa.Column('poster', sa.Text(), nullable=True),
    sa.Column('user_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['user_id'], ['user.user_id'], ),
    sa.PrimaryKeyConstraint('film_id')
    )
    op.create_table('film_director',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('director_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['director_id'], ['director.director_id'], ),
    sa.ForeignKeyConstraint(['film_id'], ['film.film_id'], ),
    sa.PrimaryKeyConstraint('film_id', 'director_id')
    )
    op.create_table('film_genre',
    sa.Column('film_id', sa.Integer(), nullable=False),
    sa.Column('genre_id', sa.Integer(), nullable=False),
    sa.ForeignKeyConstraint(['film_id'], ['film.film_id'], ),
    sa.ForeignKeyConstraint(['genre_id'], ['genre.genre_id'], ),
    sa.PrimaryKeyConstraint('film_id', 'genre_id')
    )
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_table('film_genre')
    op.drop_table('film_director')
    op.drop_table('film')
    op.drop_table('user')
    op.drop_table('genre')
    op.drop_table('director')
    # ### end Alembic commands ###
