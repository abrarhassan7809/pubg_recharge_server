from flask import Flask, jsonify, request
from scraping import Scraper

app = Flask(__name__)
scraper = Scraper()
is_login = False


@app.route('/')
def home():
    global scraper
    scraper.load_page()
    return "Welcome to the Web Scraping Flask App!"


@app.route('/get_player_name', methods=['GET'])
def get_player_name():
    global is_login
    player_id = request.args.get('player_id')
    if player_id:
        try:
            # Reset the scraper's player ID
            scraper.player_id = None

            # Login if not already logged in
            if not is_login:
                scraper.login_user()
                scraper.close_next_adds()
                is_login = True

            # Add new player ID
            is_player_id = scraper.add_player_id(player_id)
            if not is_player_id:
                player_name = scraper.get_player_name()
                return jsonify({'player_name': player_name})
            else:
                scraper.close_player_id_window()
                return jsonify({'player_id': "Invalid player id"})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error retrieving player name'}), 500
    else:
        return jsonify({'error': 'Invalid player ID'}), 400


@app.route('/get_card_data', methods=['GET'])
def get_card_data():
    player_id = request.args.get('player_id')
    item_id = request.args.get('item_id')
    if player_id and item_id:
        try:
            # Reset the scraper's player ID
            scraper.player_id = None

            # Add new player ID
            is_player_id = scraper.add_player_id(player_id)
            if not is_player_id:
                player_name = scraper.get_player_name()
                print(player_name)
                card_data = scraper.get_card_data(item_id=item_id)
                return jsonify({'card_data': card_data})
            else:
                scraper.close_player_id_window()
                return jsonify({'player_id': "Invalid player id"})
        except Exception as e:
            print(e)
            return jsonify({'error': 'Error retrieving card data'}), 500
    else:
        return jsonify({'error': 'Invalid parameters'}), 400


@app.route('/shutdown', methods=['POST'])
def shutdown():
    scraper.close_browser()
    return jsonify({'status': 'Browser closed'}), 200


if __name__ == '__main__':
    app.run(debug=True)
