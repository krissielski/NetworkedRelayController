from flask import Flask, jsonify, request
from relay_controller import RelayController
from config_manager import ConfigManager
from logger import setup_logger
import os

app = Flask(__name__)

# Global objects (to be initialized in main)
relay_controller = None
config = None
logger = None

@app.route('/relay/all/on', methods=['POST'])
def relay_all_on():
    try:
        relay_controller.turn_all_on()
        return jsonify({"status": "success", "message": "All relays turned ON"})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/relay/all/off', methods=['POST'])
def relay_all_off():
    try:
        relay_controller.turn_all_off()
        return jsonify({"status": "success", "message": "All relays turned OFF"})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/relay/<int:relay_id>/on', methods=['POST'])
def relay_on(relay_id):
    try:
        relay_controller.turn_on(relay_id)
        return jsonify({"status": "success", "relay": relay_id, "state": "ON"})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/relay/<int:relay_id>/off', methods=['POST'])
def relay_off(relay_id):
    try:
        relay_controller.turn_off(relay_id)
        return jsonify({"status": "success", "relay": relay_id, "state": "OFF"})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 400

@app.route('/relay/status', methods=['GET'])
def relay_status():
    try:
        status = relay_controller.get_status()
        return jsonify({"relays": status})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/system/version', methods=['GET'])
def system_version():
    try:
        version = config.get('system', 'version')
        build_date = None
        version_file = os.path.join(os.path.dirname(__file__), '..', 'version.txt')
        if os.path.exists(version_file):
            with open(version_file) as f:
                lines = f.readlines()
                if len(lines) > 1:
                    build_date = lines[1].strip().replace('Build date: ', '')
        return jsonify({"version": version, "build_date": build_date or "unknown"})
    except Exception as e:
        logger.error(str(e))
        return jsonify({"status": "error", "message": str(e)}), 500

@app.route('/system/health', methods=['GET'])
def system_health():
    return jsonify({"status": "healthy"})

# Initialization function for main.py

def init_api(relay_ctrl, cfg, log):
    global relay_controller, config, logger
    relay_controller = relay_ctrl
    config = cfg
    logger = log
    return app
