#!/usr/bin/env python

import sqlalchemy
from sqlalchemy import Column, Integer, String, UniqueConstraint
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.exc import IntegrityError

Base = declarative_base()

class Database():
	def __init__(self,dn_name):
		self.engine = sqlalchemy.create_engine('sqlite:///'+dn_name)
		Base.metadata.create_all(self.engine)

		self.DBSession = sessionmaker(bind=self.engine)
		self.session = self.DBSession()

	def add_record(self,record):
		try:
			self.session.add(record)
			self.session.commit()
		except:
			self.session.rollback()
			return -1

		return record.id

	def search_team(self,team):
		result=self.session.query(Team).filter_by(team_name=team).count()

		return result

	def list_teams(self):
		result=self.session.query(Team)
		teams=[]
		for team in result:
			teams.append(team.team_name)

		return teams

	def findTeamId(self,teamName):
		try:
			team_id=self.session.query(Team).filter_by(team_name=teamName)[0].id
		except IndexError:
			return -1
		return team_id

	def updateMember(self,userId,handle,phone,email):
		self.session.query(TeamMember).filter_by(id=userId).update({'user_name':handle,'user_phone':phone,'user_email':email})
		self.session.commit()
	
	def addTeamMember(self,teamName,handle,phone,email,playerType):
		team_id=self.findTeamId(teamName)

		teamMember=TeamMember(user_name=handle,user_phone=phone,
			user_email=email,team_id=team_id,member_type=playerType)
		self.add_record(teamMember)
	
	def team_members(self,team):
		ret={'hack':[],'tf2':[]}

		team_id=self.findTeamId(team)

		members=self.session.query(TeamMember).filter_by(team_id=team_id)
		if members is not None:
			for eachMember in members:
				if eachMember.member_type == 1:
					ret['hack'].append({'name':eachMember.user_name,'email':eachMember.user_email,'phone':eachMember.user_phone,'teamid':eachMember.team_id,'membertype':eachMember.member_type,'id':eachMember.id})
				else:
					ret['tf2'].append({'name':eachMember.user_name,'email':eachMember.user_email,'phone':eachMember.user_phone,'teamid':eachMember.team_id,'membertype':eachMember.member_type,'id':eachMember.id})
			return ret
		else:
			return -1
class Team(Base):
	 __tablename__ = 'team'
	 __table_args__ = (UniqueConstraint("team_name",),)

	 id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	 team_name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)

	 def __init__(self, team_name):
	 	self.team_name=team_name

class MemberType(Base):
	__tablename__ = 'membertype'
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	type_name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)

	def __init__(self, type_name):
	 	self.type_name=type_name

class TeamMember(Base):
	__tablename__ = 'teammembers'
	__table_args__ = (UniqueConstraint("user_name",),)
	id = sqlalchemy.Column(sqlalchemy.Integer, primary_key=True)
	user_name = sqlalchemy.Column(sqlalchemy.String(250), nullable=False, unique=True)
	user_email = sqlalchemy.Column(sqlalchemy.String(250), nullable=False)
	user_phone = sqlalchemy.Column(sqlalchemy.String(12), nullable=False)
	team_id = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('team.id'))
	member_type = sqlalchemy.Column(sqlalchemy.Integer, sqlalchemy.ForeignKey('membertype.id'))

	def __init__(self, user_name, user_email, user_phone, team_id, member_type):
	 	self.user_name=user_name
	 	self.user_email=user_email
	 	self.user_phone=user_phone
	 	self.team_id=team_id
	 	self.member_type=member_type



if __name__ == '__main__':
	database_connection=Database('/tmp/hf.db')
	database_connection.search_team('TEAMNAME')

	# type_hacker=MemberType("Hacker")
	# database_connection.add_record(type_hacker)

	# type_tf2=MemberType("Tf2")
	# database_connection.add_record(type_tf2)

	# team1=Team('TEAMNAME')
	# team_id=database_connection.add_record(team1)

	# team_member1=TeamMember('Bob Smith','bob@bob.com','123-456-7890',team_id,1)
	# database_connection.add_record(team_member1)

