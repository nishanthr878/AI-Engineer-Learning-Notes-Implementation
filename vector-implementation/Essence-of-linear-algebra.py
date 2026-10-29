"""
1. Computer science view : a vector is an ordered list of numbers, like (3, 4)
2. Physics view          : a vector is an arrow with a length and a direction
3. Math view             : a vector is anything you can ADD and SCALE
                             (scale = multiply by a plain number)

MATH NOTATION USED IN THE COMMENTS (so you can match code to textbook):
  v = (v1, v2, ..., vn)   a vector with n coordinates; v1 is the first one.
                          Example: v = (3, 4) means v1 = 3, v2 = 4, n = 2.
  c                       a scalar (a plain number)       -> "scalar" in code
  u, v                    two vectors                     -> "first_vector", "second_vector"
  ||v||                   the length of v (called the "norm" or "magnitude")
  v-hat                   the unit vector of v (length 1)
  sqrt(...)               square root
  v_i                     "the i-th coordinate of v"; "for all i" = "for every position"


"""

import math

class Vector:
    
    """
    A vector with any number of coordinates: 2D, 3D, 4D, ....
    """

    # Storing the vector 

    def __init__(self, *coordinates):
        """
        Runs automatically when you create a vector:  Vector(3, 4)
 
        The star in *coordinates means "accept any number of inputs and
        pack them into one tuple". So Vector(3, 4) gives coordinates=(3, 4)
        and Vector(1, 2, 3) gives coordinates=(1, 2, 3).
        """
        if len(coordinates) == 0:
            raise ValueError("A vector needs at least one coordinates")

        self.coordinates = tuple(float(number) for number in coordinates)

    @property
    def number_of_dimenstion(self):
        """
        How many coorddinates this vecot has 
        2 if arrow is 2 diemension
        3 if arrow is 3 dimenstion so on
        """

        return len(self.coordinates)

    def __repr__(self):
        """
        Printing a vector
        """
        return f"Vector {self.coordinates}"

    def __eq__(self, other_vector):
        """
        comparing two vectors
        """
        if not isinstance(other_vector, Vector):
            return False

        if self.number_of_dimenstion != other_vector.number_of_dimenstion:
            return False


        # zip pairs up the coordinates: (my_first, their_first), (my_second, their_second)...
        # all(...) is True only if EVERY pair is close enough.
        return all(
            math.isclose(my_number, their_number, abs_tol=1e-9)
            for my_number, their_number in zip(self.coordinates, other_vector.coordinates)
        )

    # The tow core operation (math view)
    # Everything else in linear algebra is built from these two.

    def __add__(self, other_vector):
        """
         Runs when you write  vector_one + vector_two.
 
        Numbers rule : add the matching coordinates.
                       (1, 2) + (3, -1) = (1+3, 2+(-1)) = (4, 1)
        Arrow rule   : "tip to tail" - place the second arrow's tail
                       at the first arrow's tip. The result is the arrow
                       from the very start to the very end.
        Both rules always give the same answer. That is the key idea of maths and physics representation of vector
        """

        self._make_sure_same_size(other_vector)
        added_coordinates = [
            my_number + their_number
            for my_number, their_number in zip(self.coordinates, other_vector.coordinates)
        ]

        return Vector(*added_coordinates)

    def __mul__(self, scalar):
        """
        Runs when you write  vector * 3.   ("scalar" = a plain number)
 
        Numbers rule : multiply EVERY coordinate by the scalar.
                       2 * (1, 2) = (2, 4)
        Arrow rule   : scalar bigger than 1  -> arrow gets longer (stretch)
                       scalar between 0 and 1 -> arrow gets shorter (squish)
                       scalar negative        -> arrow flips direction
        """

        if not isinstance(scalar, (int, float)):
            return NotImplemented

        return Vector(*[scalar * number for number in self.coordinates])

    # This line makes 3 * vector work too
    # without it, only vector * 3 wourld work.
    __rmul__ = __mul__

    # Operations build from the two above

    def __neg__(self):
        """
        Runs for -vector.
        Flipping = scaling by -1.
        """
        return self * -1

    def __sub__(self, other_vector):
        """
        Runs for vector_one - vector_two.
        """
        return self + (-other_vector)


    # Lenght and direction (physical view)

    def length(self):
        """
        How long the arrow is. This is Pythagoras' theorem:
        for (3, 4): square root of (3*3 + 4*4) = square root of 25 = 5.
        Works for any number of dimensions.
        """
        sum_of_squares = sum(number * number for number in self.coordinates)
        return math.sqrt(sum_of_squares)

    def direction(self):
        """
        An arrow pointing the SAME way but with length exactly 1
        (called a "unit vector"). Made by shrinking the vector
        by its own length.
        """
        own_lenght = self.length()
        if own_lenght == 0:
            raise ValueError("The zero vecto has no direction")

        return self * (1 / own_lenght)

    def angle_in_degrees(self):
        """
        Angle between the arrow and the right-pointing x-axis.
        Only makes sense in 2D, so refuse other sizes.
        atan2 is a math function that turns (x, y) into an angle.
        """
        if self.number_of_dimenstion != 2:
            raise ValueError("angle_in_degrees only works for 2D vectors")
        x_coordinate, y_coordinate = self.coordinates
        return math.degrees(math.atan2(y_coordinate,x_coordinate))

    def _make_sure_same_size(self, other_vector):
        """
        you cannnot add a 2D arrow to a 3D arrow. Stop with an error.
        """
        if not isinstance(other_vector, Vector):
            raise ValueError("you cann only add a vector to aonther vector")
        if other_vector.number_of_dimenstion != self.number_of_dimenstion:
            raise ValueError("Both vector mush have the same number of coordinates")


 
def run_demonstration():
    first_vector = Vector(1, 2)
    second_vector = Vector(3, -1)
 
    print("first_vector  =", first_vector)
    print("second_vector =", second_vector)
 
    print("\n--- Core operations ---")
    print("first + second   =", first_vector + second_vector)   # (4, 1)
    print("2 * first        =", 2 * first_vector)                # (2, 4)  stretched
    print("-0.5 * second    =", -0.5 * second_vector)            # (-1.5, 0.5) squished AND flipped
    print("first - second   =", first_vector - second_vector)    # (-2, 3)
 
    print("\n--- Length and direction ---")
    print("length of first        =", round(first_vector.length(), 4))
    print("direction of first     =", first_vector.direction())
    print("length of that direction =", round(first_vector.direction().length(), 4), "(always 1)")
    print("angle of first         =", round(first_vector.angle_in_degrees(), 2), "degrees")
 
    # The "math view" says: a vector is anything obeying these rules.
    # "assert" means: "I claim this is true. Crash loudly if it is not."
    print("\n--- Checking the rules every vector must obey ---")
    zero_vector = Vector(0, 0)
    third_vector = Vector(-2, 5)
 
    assert first_vector + second_vector == second_vector + first_vector          # order doesn't matter
    assert (first_vector + second_vector) + third_vector == first_vector + (second_vector + third_vector)  # grouping doesn't matter
    assert first_vector + zero_vector == first_vector                            # adding nothing changes nothing
    assert first_vector + (-first_vector) == zero_vector                         # a vector plus its flip cancels out
    assert 3 * (first_vector + second_vector) == 3 * first_vector + 3 * second_vector  # scale spreads over addition
    assert (2 + 3) * first_vector == 2 * first_vector + 3 * first_vector         # scalars add up
    assert 2 * (3 * first_vector) == (2 * 3) * first_vector                      # scaling twice = scaling once by the product
    assert 1 * first_vector == first_vector                                      # scaling by 1 changes nothing
    print("All rules hold.")
 
    print("\n--- Same code works in 4 dimensions ---")
    four_d_one = Vector(1, 2, 3, 4)
    four_d_two = Vector(4, 3, 2, 1)
    print("sum    =", four_d_one + four_d_two)
    print("length =", round(four_d_one.length(), 4))
 
 
def draw_tip_to_tail_picture(first_vector, second_vector):
    """
    OPTIONAL: draws the picture from the video and saves it as a PNG.
    Needs matplotlib:  pip install matplotlib
    Blue arrow   = first vector, from the origin
    Orange arrow = second vector, moved so its tail sits on the blue arrow's tip
    Green arrow  = the sum, from the origin straight to the orange arrow's tip
    """
    import matplotlib.pyplot as plt
 
    sum_vector = first_vector + second_vector
    figure, axes = plt.subplots()
 
    arrow_style = dict(angles="xy", scale_units="xy", scale=1)
    axes.quiver(0, 0, *first_vector.coordinates, color="tab:blue", label="first", **arrow_style)
    axes.quiver(*first_vector.coordinates, *second_vector.coordinates, color="tab:orange", label="second (moved)", **arrow_style)
    axes.quiver(0, 0, *sum_vector.coordinates, color="tab:green", label="first + second", **arrow_style)
 
    limit = max(abs(number) for number in (*first_vector.coordinates, *sum_vector.coordinates)) + 1
    axes.set_xlim(-1, limit)
    axes.set_ylim(-limit, limit)
    axes.axhline(0, color="gray", linewidth=0.5)
    axes.axvline(0, color="gray", linewidth=0.5)
    axes.set_aspect("equal")
    axes.grid(alpha=0.3)
    axes.legend()
    plt.savefig("tip_to_tail.png", dpi=120)
 
 
# This block runs only when you start THIS file ("python vectors_beginner.py"),
# not when another file imports it.
if __name__ == "__main__":
    run_demonstration()
    try:
        draw_tip_to_tail_picture(Vector(1, 2), Vector(3, -1))
        print("\nSaved tip_to_tail.png")
    except ImportError:
        print("\n(matplotlib not installed - skipping the picture)")  



    
        

    



