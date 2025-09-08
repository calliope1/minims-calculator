from flask import jsonify
import compute.minims_calculator as mc

def return_minims(request) -> dict:
    """Return all possible words from the minim expression.

    Arguments
    ---------
        expression
            Minims string expression.

    Returns
    -------
        dict (JSON)
            With 'error' if there is a missing parameter or computation error.
            With 'results' otherwise, having a JSON array of all possible words.
    """

    expression = request.args.get('expression', '')
    if not expression:
        return jsonify({'error': 'Missing expression parameter'}), 400
    try:
	# Using all caps
        result = mc.compute_minims(expression.upper())
        return jsonify({'results': result}), 200
    except Exception as e:
        return jsonify({'error': 'Computation error', 'details': str(e)}), 500