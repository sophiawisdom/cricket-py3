## n is the degree.  If n == 3, the b-spline is cubic.
## m := len( P ) - 1
## len( knots ) == len( P ) + n + 1
## t is the parameter along the curve.  t is in [0,1].

def b_j_n( knots, j, n, t ):
    if n == 0:
        if knots[j] <= t and t < knots[j+1]: return 1.
        else: return 0.

    lhs_coeff_numer = t - knots[j]
    lhs_coeff_denom = knots[j+n] - knots[j]
    if lhs_coeff_numer != 0. and lhs_coeff_denom != 0.:
        lhs = ( lhs_coeff_numer / lhs_coeff_denom ) * b_j_n( knots, j, n-1, t )
    else:
        lhs = 0.

    rhs_coeff_numer = knots[j+n+1] - t
    rhs_coeff_denom = knots[j+n+1] - knots[j+1]
    if rhs_coeff_numer != 0. and rhs_coeff_denom != 0.:
        rhs = ( rhs_coeff_numer / rhs_coeff_denom ) * b_j_n( knots, j+1, n-1, t )
    else:
        rhs = 0.

    return lhs + rhs

def S( knots, n, P, t ):

    m = len( P ) - 1
    assert len( knots ) == len( P ) + n + 1

    from numpy import zeros
    result = zeros( len( P[0] ) )
    for i in range( len(P) ):
        result += P[i] * b_j_n( knots, i, n, t )

    return result

def uniform_knots( num_pts, degree ):
    '''
    A helper function for Uniform B-Splines.
    Returns an evenly spaced knot vector for passing to S().
    '''
    assert num_pts > 1

    from numpy import linspace
    return linspace( 0, 1, num_pts + degree + 1 )

def magic_uniform_knots( num_pts, degree ):
    '''
    Like uniform knots, but returns knots shifted and scaled
    such that t in [0,1] is evaluatable.
    '''

    assert num_pts + 1 > degree
    assert degree > 1

    knots = uniform_knots( num_pts, degree )

    n = degree

    k0 = n
    k1 = len( knots )-1 - n

    shift = -knots[k0]
    scale = 1. / ( knots[k1] - knots[k0] )

    knots += shift
    knots *= scale

    return knots


def Uniform_B_Spline( P, n ):
    '''
    Returns a function object that can be called with parameters between 0 and 1
    to evaluate the B-Spline with control points 'P' and degree 'n'.
    '''

    if len(P) <= n: return lambda t: P[ len(P) // 2 ]

    knots = magic_uniform_knots( len( P ), n )
    #knots = uniform_knots( len( P ), n )
    return lambda t: S( knots, n, P, t )


def S_3_i( P, i, t ):
    '''
    Returns the evaluation of a cubic b-spline S evaluated at index 'i', 1 <= i < len(P) - 2,
    and parameter t, 0 <= t <= 1.
    '''

    assert i - 1 >= 0
    assert i + 2 < len(P)

    from numpy import array, dot
    A = array( [[ -1, 3, -3, 1 ], [ 3, -6, 3, 0 ], [ -3, 0, 3, 0 ], [ 1, 4, 1, 0 ]] )
    ps = P[i-1:i+3]
    ts = array( [ t**3, t**2, t, 1 ] )

    return 1./6. * dot( ts, dot( A, ps ) )

def S_3( P, t ):
    '''
    Returns the evaluation of a cubic b-spline S evaluated at t, 0 <= t <= 1.
    '''

    from math import floor

    a = 1
    b = len(P) - 2

    texpand = a + t*(b-a)
    i = min( int( floor( texpand ) ), len(P) - 3 )
    tt = texpand - i

    return S_3_i( P, i, tt )

def Uniform_Cubic_B_Spline( P ):
    '''
    Returns a function object that can be called with parameters between 0 and 1
    to evaluate the uniform, cubic B-Spline with control points 'P'.
    '''

    if len(P) < 4: return lambda t: P[ len(P)//2 ]

    return lambda t: S_3( P, t )


def test1():
    print('====== test1() ======')

    from numpy import meshgrid, linspace
    P = meshgrid([0,0],list(range(10)))[1]

    degree = 3
    bspline = Uniform_B_Spline( P, degree )
    V = 5
    for val in linspace( 0, 1, V ):
        print(('%s: %s' % (val, bspline( val ))))

def test2():
    print('====== test2() ======')

    from numpy import meshgrid, linspace
    P = meshgrid([0,0],list(range(10)))[1]

    bspline = Uniform_Cubic_B_Spline( P )
    V = 5
    for val in linspace( 0, 1, V ):
        print(('%s: %s' % (val, bspline( val ))))

def main():
    test1()
    test2()

if __name__ == '__main__': main()
