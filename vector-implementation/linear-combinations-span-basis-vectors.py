"""
Essence of Linear Algebra - Chapter 2: Linear combinations, span and basis vectors
===================================================================================

This script turns the five key points of the lecture into small, runnable Python
examples. It uses only plain Python (no extra libraries to install).

How to run:
    python3 essence_of_linear_algebra_chapter_2.py

How vectors are stored:
    A two dimensional vector is a tuple of two numbers:
        (horizontal_component, vertical_component)
    Example: (3, -2) means "3 steps to the right, 2 steps down".
"""

# A very small number used when comparing decimal numbers, because computers
# store decimals approximately (for example 0.1 + 0.2 is not exactly 0.3).
TOLERANCE_FOR_DECIMAL_COMPARISON = 1e-9


# =============================================================================
# BUILDING BLOCKS: the two basic vector operations
# =============================================================================

def scale_vector(scalar, vector):
    """
    Stretch or shrink a vector by a number (called a scalar).

    Formula:
        scalar * (horizontal, vertical) = (scalar * horizontal, scalar * vertical)

    A negative scalar also flips the vector to point the opposite way.
    """
    horizontal_component, vertical_component = vector
    return (scalar * horizontal_component, scalar * vertical_component)


def add_vectors(first_vector, second_vector):
    """
    Add two vectors by adding their matching components.

    Formula:
        (a, b) + (c, d) = (a + c, b + d)

    Picture: walk along the first vector, then walk along the second vector.
    """
    first_horizontal, first_vertical = first_vector
    second_horizontal, second_vertical = second_vector
    return (first_horizontal + second_horizontal,
            first_vertical + second_vertical)


# =============================================================================
# POINT 1: LINEAR COMBINATION
# =============================================================================

def linear_combination(first_scalar, first_vector, second_scalar, second_vector):
    """
    Scale two vectors and then add them together.

    Formula:
        linear combination = first_scalar * first_vector
                           + second_scalar * second_vector

    The two scalars are the "coordinates" of the result when the two vectors
    are used as the basis vectors.
    """
    scaled_first_vector = scale_vector(first_scalar, first_vector)
    scaled_second_vector = scale_vector(second_scalar, second_vector)
    return add_vectors(scaled_first_vector, scaled_second_vector)


def show_linear_combination_section():
    print("=" * 70)
    print("POINT 1: LINEAR COMBINATION")
    print("=" * 70)
    print("Formula: linear combination = a * v + b * w")
    print("(scale vector v by a, scale vector w by b, then add the results)\n")

    first_vector = (1, 2)
    second_vector = (3, 1)

    for first_scalar, second_scalar in [(1, 1), (2, 1), (-1, 3), (0.5, -2)]:
        result = linear_combination(first_scalar, first_vector,
                                    second_scalar, second_vector)
        print(f"  {first_scalar} * {first_vector} + {second_scalar} * {second_vector}"
              f"  =  {result}")
    print()


# =============================================================================
# POINT 2: BASIS VECTORS AND COORDINATES
# =============================================================================

def show_basis_vectors_section():
    print("=" * 70)
    print("POINT 2: BASIS VECTORS")
    print("=" * 70)
    print("Coordinates are scalars that scale the basis vectors.\n")

    # i-hat points one step right, j-hat points one step up.
    basis_vector_i_hat = (1, 0)
    basis_vector_j_hat = (0, 1)

    horizontal_coordinate = 3
    vertical_coordinate = -2
    vector_from_standard_basis = linear_combination(
        horizontal_coordinate, basis_vector_i_hat,
        vertical_coordinate, basis_vector_j_hat)

    print("Standard basis: i-hat = (1, 0) and j-hat = (0, 1)")
    print(f"  Coordinates ({horizontal_coordinate}, {vertical_coordinate}) mean:")
    print(f"  {horizontal_coordinate} * i-hat + {vertical_coordinate} * j-hat"
          f" = {vector_from_standard_basis}\n")

    # The same coordinates give a DIFFERENT vector if we choose a different basis.
    # Any two vectors that do not point along the same line can act as a basis.
    new_first_basis_vector = (2, 1)
    new_second_basis_vector = (-1, 2)
    coordinates = (-1, 2)
    vector_from_new_basis = linear_combination(
        coordinates[0], new_first_basis_vector,
        coordinates[1], new_second_basis_vector)

    print(f"A different basis: {new_first_basis_vector} and {new_second_basis_vector}")
    print(f"  The same coordinates {coordinates} now mean:")
    print(f"  {coordinates[0]} * {new_first_basis_vector} + "
          f"{coordinates[1]} * {new_second_basis_vector} = {vector_from_new_basis}")
    print("  Same coordinates, different basis, different vector.\n")


# =============================================================================
# POINT 4 (needed first): LINEAR DEPENDENCE CHECK
# =============================================================================

def is_zero_vector(vector):
    """A zero vector is (0, 0). It has no length and no direction."""
    horizontal_component, vertical_component = vector
    return (abs(horizontal_component) < TOLERANCE_FOR_DECIMAL_COMPARISON and
            abs(vertical_component) < TOLERANCE_FOR_DECIMAL_COMPARISON)


def are_linearly_dependent(first_vector, second_vector):
    """
    Two vectors are linearly dependent when one of them is redundant, meaning
    it can be written as a scaled copy of the other:

        second_vector = scalar * first_vector

    Then the second vector lies on the same line and adds no new dimension.
    A zero vector is always redundant, because it adds nothing.
    """
    if is_zero_vector(first_vector) or is_zero_vector(second_vector):
        return True

    # Work out which scalar would turn the first vector into the second one.
    # We divide using a component that is not zero, to avoid dividing by zero.
    first_horizontal, first_vertical = first_vector
    second_horizontal, second_vertical = second_vector
    if abs(first_horizontal) > TOLERANCE_FOR_DECIMAL_COMPARISON:
        scalar = second_horizontal / first_horizontal
    else:
        scalar = second_vertical / first_vertical

    # Check: does scalar * first_vector really equal second_vector?
    scaled_first_vector = scale_vector(scalar, first_vector)
    horizontal_difference = abs(scaled_first_vector[0] - second_horizontal)
    vertical_difference = abs(scaled_first_vector[1] - second_vertical)
    return (horizontal_difference < TOLERANCE_FOR_DECIMAL_COMPARISON and
            vertical_difference < TOLERANCE_FOR_DECIMAL_COMPARISON)


def are_linearly_independent(first_vector, second_vector):
    """Independent means: every vector adds a new dimension to the span."""
    return not are_linearly_dependent(first_vector, second_vector)


# =============================================================================
# POINT 3: SPAN
# =============================================================================

def collect_span_points(first_vector, second_vector, largest_scalar=12,
                        scalar_step=1):
    """
    Sample the span of two vectors.

    The span is the set of ALL vectors reachable with:
        a * first_vector + b * second_vector     for every possible a and b

    There are infinitely many choices for a and b, so the computer can only
    try a sample: here every whole number from -largest_scalar to +largest_scalar.
    (The sample range is large enough to cover the whole drawn grid. A smaller
    range would leave gaps that look empty only because we did not try
    enough scalars, not because those points are truly unreachable.)
    """
    reachable_points = set()
    scalar = -largest_scalar
    while scalar <= largest_scalar:
        other_scalar = -largest_scalar
        while other_scalar <= largest_scalar:
            point = linear_combination(scalar, first_vector,
                                       other_scalar, second_vector)
            reachable_points.add(point)
            other_scalar += scalar_step
        scalar += scalar_step
    return reachable_points


def draw_span_grid(reachable_points, grid_half_size=6):
    """
    Draw a small text picture of the plane.
        O = the origin (0, 0)
        # = a point reachable by a linear combination
        . = a point not reached by our sample
    """
    for vertical_position in range(grid_half_size, -grid_half_size - 1, -1):
        row_of_symbols = []
        for horizontal_position in range(-grid_half_size, grid_half_size + 1):
            point = (horizontal_position, vertical_position)
            if point == (0, 0):
                row_of_symbols.append("O")
            elif point in reachable_points:
                row_of_symbols.append("#")
            else:
                row_of_symbols.append(".")
        print("    " + " ".join(row_of_symbols))


def show_span_section():
    print("=" * 70)
    print("POINT 3: SPAN")
    print("=" * 70)
    print("Span = every vector you can reach with a * v + b * w,")
    print("over all possible choices of the scalars a and b.\n")

    examples = [
        ("Two vectors NOT on the same line -> span fills the whole plane",
         (1, 0), (1, 1)),
        ("Two vectors on the SAME line -> span is only that line",
         (1, 2), (2, 4)),
        ("Both vectors are the zero vector -> span is only the origin",
         (0, 0), (0, 0)),
    ]

    for description, first_vector, second_vector in examples:
        reachable_points = collect_span_points(first_vector, second_vector)
        print(f"{description}")
        print(f"  first vector = {first_vector}, second vector = {second_vector}")
        draw_span_grid(reachable_points)
        print()


# =============================================================================
# POINT 4: LINEAR DEPENDENCE VERSUS INDEPENDENCE
# =============================================================================

def show_linear_dependence_section():
    print("=" * 70)
    print("POINT 4: LINEAR DEPENDENCE VERSUS INDEPENDENCE")
    print("=" * 70)
    print("Dependent  : one vector is redundant (it is already in the span of the others).")
    print("Independent: every vector adds a new dimension to the span.\n")

    pairs_to_test = [
        ((1, 2), (2, 4)),    # second = 2 * first         -> dependent
        ((1, 2), (-3, -6)),  # second = -3 * first        -> dependent
        ((1, 0), (0, 1)),    # point in different ways    -> independent
        ((1, 2), (3, 1)),    # point in different ways    -> independent
    ]
    for first_vector, second_vector in pairs_to_test:
        if are_linearly_dependent(first_vector, second_vector):
            verdict = "linearly DEPENDENT   (one is a scaled copy of the other)"
        else:
            verdict = "linearly INDEPENDENT (each adds a new dimension)"
        print(f"  {first_vector} and {second_vector}: {verdict}")

    # Three vectors in a flat plane: the third is always redundant, because
    # the first two vectors already reach every point in the plane.
    print("\nThree vectors in a flat plane:")
    first_vector = (1, 0)
    second_vector = (0, 1)
    third_vector = linear_combination(2, first_vector, 3, second_vector)
    print(f"  first = {first_vector}, second = {second_vector}, third = {third_vector}")
    print(f"  third = 2 * first + 3 * second = {third_vector}")
    print("  The third vector is already inside the span of the first two,")
    print("  so it is redundant and the three vectors are linearly dependent.\n")


# =============================================================================
# POINT 5: DEFINITION OF A BASIS
# =============================================================================

def is_basis_for_plane(first_vector, second_vector):
    """
    Definition: a basis of a space is a set of linearly independent vectors
    that span that space.

    For a flat two dimensional plane, two linearly independent vectors are
    enough to reach every point, so they form a basis.
    """
    return are_linearly_independent(first_vector, second_vector)


def show_basis_definition_section():
    print("=" * 70)
    print("POINT 5: DEFINITION OF A BASIS")
    print("=" * 70)
    print("Basis = a set of linearly independent vectors that span the space.\n")

    candidates = [
        ((1, 0), (0, 1)),
        ((2, 1), (-1, 2)),
        ((1, 2), (2, 4)),
        ((0, 0), (1, 1)),
    ]
    for first_vector, second_vector in candidates:
        if is_basis_for_plane(first_vector, second_vector):
            verdict = "YES, a basis (independent, and together they span the plane)"
        else:
            verdict = "NO, not a basis (one vector is redundant, span is not the plane)"
        print(f"  {first_vector} and {second_vector}: {verdict}")
    print()


# =============================================================================
# RUN EVERYTHING
# =============================================================================

if __name__ == "__main__":
    show_linear_combination_section()
    show_basis_vectors_section()
    show_span_section()
    show_linear_dependence_section()
    show_basis_definition_section()