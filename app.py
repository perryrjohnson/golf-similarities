from flask import Flask, request, render_template, Response
import pandas as pd
import turicreate as tc
import pickle
import random
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')
pgatour_players = tc.SFrame('Data/pgatour_stats.csv')
content_model = tc.load_model('player_skill_recommender')


app = Flask(__name__)


@app.route('/')
def home():
	players = list(pgatour_players['NAME'])
	return render_template('choose-player.html', players=players)

@app.route('/scoring-method')
def scoring():
	return render_template('scoring-method.html')		

@app.route('/make-recommendations', methods=['POST', 'GET'])
def get_recommendations():
	player = request.form.get('player-name')
	if player in list(pgatour_players['NAME']): 
		recs = content_model.recommend_from_interactions(observed_items=[player], k=5)	
		your_player = player
		return render_template('make-recommendations.html', your_player=your_player, recs=recs)		
	else:	
		return render_template('error.html')

if __name__ == '__main__':
	app.run()
