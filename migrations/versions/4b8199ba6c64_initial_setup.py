"""Initial Setup

Revision ID: 4b8199ba6c64
Revises: 
Create Date: 2020-11-01 18:24:12.439070

"""
from alembic import op
import sqlalchemy as sa


# revision identifiers, used by Alembic.
revision = '4b8199ba6c64'
down_revision = None
branch_labels = None
depends_on = None


def upgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.create_table('device_type',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('brand', sa.String(length=30), nullable=True),
    sa.Column('model', sa.String(length=30), nullable=True),
    sa.Column('hardware_category', sa.String(length=30), nullable=True),
    sa.Column('netmiko_category', sa.Text(), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_type_brand'), 'device_type', ['brand'], unique=False)
    op.create_index(op.f('ix_device_type_hardware_category'), 'device_type', ['hardware_category'], unique=False)
    op.create_index(op.f('ix_device_type_model'), 'device_type', ['model'], unique=False)
    op.create_index(op.f('ix_device_type_netmiko_category'), 'device_type', ['netmiko_category'], unique=False)
    op.create_table('proxy_settings',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('proxy_name', sa.String(length=25), nullable=True),
    sa.Column('proxy_settings', sa.String(length=255), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_proxy_settings_proxy_name'), 'proxy_settings', ['proxy_name'], unique=True)
    op.create_index(op.f('ix_proxy_settings_proxy_settings'), 'proxy_settings', ['proxy_settings'], unique=True)
    op.create_table('user',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('nickname', sa.String(length=64), nullable=True),
    sa.Column('email', sa.String(length=120), nullable=True),
    sa.Column('username', sa.String(length=15), nullable=True),
    sa.Column('password', sa.String(length=20), nullable=True),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_user_email'), 'user', ['email'], unique=True)
    op.create_index(op.f('ix_user_nickname'), 'user', ['nickname'], unique=True)
    op.create_index(op.f('ix_user_password'), 'user', ['password'], unique=False)
    op.create_index(op.f('ix_user_username'), 'user', ['username'], unique=True)
    op.create_table('device',
    sa.Column('id', sa.Integer(), nullable=False),
    sa.Column('hostname', sa.String(length=64), nullable=True),
    sa.Column('ipv4_addr', sa.String(length=15), nullable=True),
    sa.Column('ios_type', sa.String(length=15), nullable=True),
    sa.Column('local_creds', sa.Boolean(), nullable=True),
    sa.Column('devicetype_id', sa.Integer(), nullable=True),
    sa.Column('proxy_id', sa.Integer(), nullable=True),
    sa.ForeignKeyConstraint(['devicetype_id'], ['device_type.id'], ),
    sa.ForeignKeyConstraint(['proxy_id'], ['proxy_settings.id'], ),
    sa.PrimaryKeyConstraint('id')
    )
    op.create_index(op.f('ix_device_hostname'), 'device', ['hostname'], unique=True)
    op.create_index(op.f('ix_device_ios_type'), 'device', ['ios_type'], unique=False)
    op.create_index(op.f('ix_device_ipv4_addr'), 'device', ['ipv4_addr'], unique=True)
    # ### end Alembic commands ###


def downgrade():
    # ### commands auto generated by Alembic - please adjust! ###
    op.drop_index(op.f('ix_device_ipv4_addr'), table_name='device')
    op.drop_index(op.f('ix_device_ios_type'), table_name='device')
    op.drop_index(op.f('ix_device_hostname'), table_name='device')
    op.drop_table('device')
    op.drop_index(op.f('ix_user_username'), table_name='user')
    op.drop_index(op.f('ix_user_password'), table_name='user')
    op.drop_index(op.f('ix_user_nickname'), table_name='user')
    op.drop_index(op.f('ix_user_email'), table_name='user')
    op.drop_table('user')
    op.drop_index(op.f('ix_proxy_settings_proxy_settings'), table_name='proxy_settings')
    op.drop_index(op.f('ix_proxy_settings_proxy_name'), table_name='proxy_settings')
    op.drop_table('proxy_settings')
    op.drop_index(op.f('ix_device_type_netmiko_category'), table_name='device_type')
    op.drop_index(op.f('ix_device_type_model'), table_name='device_type')
    op.drop_index(op.f('ix_device_type_hardware_category'), table_name='device_type')
    op.drop_index(op.f('ix_device_type_brand'), table_name='device_type')
    op.drop_table('device_type')
    # ### end Alembic commands ###