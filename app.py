from flask import Flask, jsonify, request
from scraping import Scraper, CardScraper

app = Flask(__name__)


@app.route('/')
def home():
    return "Welcome to the Web Scraping Flask App!"


@app.route('/get_player_name', methods=['GET'])
def user_login():
    player_id = request.args.get('player_id')
    if player_id:
        try:
            scraper = Scraper(player_id=player_id)
            player_name = scraper.run()
            return jsonify({'player_name': player_name})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Player not found'}), 404
    else:
        return jsonify({'error': 'Invalid Player Id'}), 400


@app.route('/get_card_data', methods=['GET'])
def get_card_data():
    player_id = request.args.get("player_id")
    item_id = request.args.get("item_id")
    print(player_id, item_id)
    try:
        scraper = CardScraper(player_id=player_id, item_id=item_id)
        card_data = scraper.run()
        return jsonify({'cards data': card_data})
    except Exception as e:
        print(e)
        return jsonify({'error': 'Card data not found'}), 404


if __name__ == '__main__':
    app.run(debug=True)
