from flask import Flask, request, render_template, Response
import pandas as pd
import turicreate as tc
import pickle
import random
import sys
import json

reload(sys)
sys.setdefaultencoding('utf8')
scaled_stats = tc.SFrame('Data/scaled_stats.csv')
raw_stats = tc.SFrame('Data/raw_stats.csv')
content_model = tc.load_model('player_skill_recommender')


app = Flask(__name__)

def get_info(player):
	data = raw_stats[raw_stats['NAME']==player]
	return data


@app.route('/')
def home():
	players = list(scaled_stats['NAME'])
	return render_template('choose-player.html', players=players)

@app.route('/scoring-method')
def scoring():
	return render_template('scoring-method.html')		

@app.route('/make-recommendations', methods=['POST', 'GET'])
def get_recommendations():
	player = request.form.get('player-name')
	if player in list(scaled_stats['NAME']):
		recs = content_model.recommend_from_interactions(observed_items=[player], k=5)
		player_data = []
		for rec in recs:
			name = rec['NAME']
			info = get_info(name)
			info['score'] = "{:.2}".format(rec['score'])
			player_data.append(info)
		your_player=get_info(player)	
		return render_template('make-recommendations.html', your_player=your_player, recs=player_data)		
	else:	
		return render_template('error.html')

if __name__ == '__main__':
	app.run()
