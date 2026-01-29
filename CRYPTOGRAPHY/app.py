from flask import Flask, render_template, request, jsonify, session
import secrets

app = Flask(__name__)
app.secret_key = secrets.token_hex(16)  # For session management


def generate_shifted_alphabet(shift):
    """
    Generate shifted alphabet for visualization
    """
    alphabet_original = [chr(i) for i in range(ord('A'), ord('Z') + 1)]
    alphabet_shifted = []

    for i in range(len(alphabet_original)):
        shifted_index = (i + shift) % 26
        alphabet_shifted.append(alphabet_original[shifted_index])

    return alphabet_original, alphabet_shifted


def caesar_cipher(text, shift, mode='encrypt'):
    """
    Encrypt or decrypt text using Caesar cipher

    Args:
        text: The text to process
        shift: Number of positions to shift (1-25)
        mode: 'encrypt' or 'decrypt'

    Returns:
        The processed text
    """
    if mode == 'decrypt':
        shift = -shift

    result = ""

    for char in text:
        if char.isalpha():
            # Determine the base for uppercase or lowercase
            base = ord('A') if char.isupper() else ord('a')
            # Apply the shift and wrap around the alphabet
            shifted_char = chr((ord(char) - base + shift) % 26 + base)
            result += shifted_char
        else:
            # Keep non-alphabetic characters as they are
            result += char

    return result


@app.route('/')
def index():
    """Render the main page"""
    # Default shift value
    default_shift = session.get('last_shift', 5)
    original_alphabet, shifted_alphabet = generate_shifted_alphabet(default_shift)

    return render_template('index.html',
                           shift=default_shift,
                           original_alphabet=original_alphabet,
                           shifted_alphabet=shifted_alphabet)


@app.route('/encrypt', methods=['POST'])
def encrypt():
    """Encrypt text using Caesar cipher"""
    try:
        data = request.get_json()
        plaintext = data.get('text', '')
        shift = int(data.get('shift', 5))

        # Validate shift value
        if shift < 1 or shift > 25:
            return jsonify({'error': 'Shift value must be between 1 and 25'}), 400

        if not plaintext:
            return jsonify({'error': 'No text provided'}), 400

        # Generate shifted alphabet for visualization
        original_alphabet, shifted_alphabet = generate_shifted_alphabet(shift)

        # Store shift in session
        session['last_shift'] = shift

        # Process the text
        ciphertext = caesar_cipher(plaintext, shift, 'encrypt')

        return jsonify({
            'original_text': plaintext,
            'encrypted_text': ciphertext,
            'shift': shift,
            'original_alphabet': original_alphabet,
            'shifted_alphabet': shifted_alphabet
        })
    except ValueError:
        return jsonify({'error': 'Invalid shift value. Must be a number between 1 and 25.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/decrypt', methods=['POST'])
def decrypt():
    """Decrypt text using Caesar cipher"""
    try:
        data = request.get_json()
        ciphertext = data.get('text', '')
        shift = int(data.get('shift', 5))

        # Validate shift value
        if shift < 1 or shift > 25:
            return jsonify({'error': 'Shift value must be between 1 and 25'}), 400

        if not ciphertext:
            return jsonify({'error': 'No text provided'}), 400

        # Generate shifted alphabet for visualization
        original_alphabet, shifted_alphabet = generate_shifted_alphabet(shift)

        # Store shift in session
        session['last_shift'] = shift

        # Process the text
        plaintext = caesar_cipher(ciphertext, shift, 'decrypt')

        return jsonify({
            'encrypted_text': ciphertext,
            'decrypted_text': plaintext,
            'shift': shift,
            'original_alphabet': original_alphabet,
            'shifted_alphabet': shifted_alphabet
        })
    except ValueError:
        return jsonify({'error': 'Invalid shift value. Must be a number between 1 and 25.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/encrypt', methods=['GET'])
def api_encrypt():
    """API endpoint for encryption via GET request"""
    try:
        text = request.args.get('text', '')
        shift = int(request.args.get('shift', 5))

        # Validate shift value
        if shift < 1 or shift > 25:
            return jsonify({'error': 'Shift value must be between 1 and 25'}), 400

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        ciphertext = caesar_cipher(text, shift, 'encrypt')

        return jsonify({
            'original_text': text,
            'encrypted_text': ciphertext,
            'shift': shift
        })
    except ValueError:
        return jsonify({'error': 'Invalid shift value. Must be a number between 1 and 25.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


@app.route('/api/decrypt', methods=['GET'])
def api_decrypt():
    """API endpoint for decryption via GET request"""
    try:
        text = request.args.get('text', '')
        shift = int(request.args.get('shift', 5))

        # Validate shift value
        if shift < 1 or shift > 25:
            return jsonify({'error': 'Shift value must be between 1 and 25'}), 400

        if not text:
            return jsonify({'error': 'No text provided'}), 400

        plaintext = caesar_cipher(text, shift, 'decrypt')

        return jsonify({
            'encrypted_text': text,
            'decrypted_text': plaintext,
            'shift': shift
        })
    except ValueError:
        return jsonify({'error': 'Invalid shift value. Must be a number between 1 and 25.'}), 400
    except Exception as e:
        return jsonify({'error': str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True, port=5000)