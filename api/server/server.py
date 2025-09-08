from flask import jsonify
import compute.minims_calculator as mc

def return_minims(request, path : str, max_n : int) -> dict:
    """Return all possible words from the minim expression.

    Uses mc.file_compute_minims, which is necessarily memoized.

    Arguments
    ---------
    expression
        Minims string expression.
    path : str
        Path to data files being calculated/pre-calculated
    max_n : int
        Maximum n for which minims-<n>.json will be created by file_minims_calculate

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
        result = mc.file_compute_minims(expression.upper(), path, max_n)
        return jsonify({'results': result}), 200
    except Exception as e:
        return jsonify({'error': 'Computation error', 'details': str(e)}), 500