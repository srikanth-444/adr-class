import numpy as np

def ekf_prediction(x_old, P_old, v, delta, L, dt):
    # Inputs:
    #   x_old: Previous state estimate [x; y; theta]
    #   P_old: Previous covariance matrix
    #   v: Linear velocity of the vehicle (forward speed)
    #   delta: Steering angle of the front wheels
    #   L: Distance between the front and rear axles (wheelbase)
    #   dt: Time step

    # State transition matrix Jacobian (H)
    H = np.eye(3)  # Identity matrix since state transition is nonlinear

    # Control input matrix (B)
    B = np.array([[np.cos(x_old[2]) * dt, 0],
                  [np.sin(x_old[2]) * dt, 0],
                  [0, v / L * dt]])  # Linearize control input but we need to change this accordingly

    # Motion model
    x, y, theta = x_old

    # Linear displacement
    delta_x = v * np.cos(theta) * dt
    delta_y = v * np.sin(theta) * dt

    # Angular displacement
    delta_theta = (v / L) * np.tan(delta) * dt

    # Update state
    x_new = x_old + np.array([delta_x, delta_y, delta_theta])

    # Jacobian of the motion model with respect to state (H)
    G = np.array([[1, 0, -v * np.sin(theta) * dt],
                  [0, 1, v * np.cos(theta) * dt],
                  [0, 0, 1]])

    # Process noise covariance matrix (Q)
    Q = np.zeros((3, 3))  # no process noise

    # Predicted covariance matrix
    P_new = np.dot(G, np.dot(P_old, G.T)) + np.dot(B, np.dot(Q, B.T))

    return x_new, P_new
