## Here we do the optimization operations.

# Calulcate the min variance portfolio for effecient frontier's SD and riskpremium
import scipy.optimize as optimize
import math

def calc_risk_premium(wts, er):
    risk_prem = wts @ er
    return risk_prem
    
covar = var_covar.to_numpy()
def objective_function(x):
    iter_weights = np.array([x[0],x[1], x[2], 1-x[0]-x[1]-x[2]])
    return np.power((iter_weights @ covar) @ iter_weights.T ,0.5)

def constraint_risk_prem(x, target):
    iter_weights = np.array([x[0],x[1], x[2], 1-x[0]-x[1]-x[2]])
    return_distr_risk_premium = np.array([[return_dist[r][0]] for r in return_dist.keys()])
    risk_prem = calc_risk_premium(iter_weights, return_distr_risk_premium)
    # print(target, risk_prem)
    return risk_prem - target

# def x0(x):
#     return x[0]
# def x1(x):
#     return x[1]
# def x2(x):
#     return x[2]
# def x3(x):
#     return x[3]

def total_one(x):
    return (x[0] + x[1] + x[2]) - 1

ineq_constraint = {'type': 'ineq', 'fun': total_one}
# Create the constraint object
# total_one_constr = optimize.NonlinearConstraint(total_one, 0, 0)

# cons = [
#     {'type':'eq', 'fun': total_one},
#     # {'type':'eq', 'fun': x0},
#     # {'type':'eq', 'fun': x1},
#     # {'type':'eq', 'fun': x2},
#     # {'type':'eq', 'fun': x3}
# ]

bounds = [(0,1),(0,1),(0,1)]

# Initial guess
initial_values = np.array([0.1, 0.2, 0.3])

# Call the minimize function
result = scipy.optimize.minimize(objective_function, initial_values, constraints=[ineq_constraint], method='SLSQP', bounds=bounds)
x = result.x
full_x = [x[0],x[1], x[2], 1-x[0]-x[1]-x[2]]
# Print the result
print("min SD for efficient frontier:", result.fun)
print("optimized weights: ", full_x)

risk_prem = np.array(full_x) @ np.array([[return_dist[r][0]] for r in return_dist.keys()])
print("risk prem for efficient frontier 1st line.",risk_prem)

changing_wts = x
next_risk_prem = math.ceil(risk_prem.item() * 100)
for val in range(next_risk_prem, next_risk_prem + 8):
    target_risk_prem = val * 0.01
    print(target_risk_prem)
    
    cons = [
    {'type':'eq', 'fun': total_one},
    # {'type':'eq', 'fun': lambda x: constraint_risk_prem(x,target_risk_prem)},
    # {'type':'eq', 'fun': x1},
    # {'type':'eq', 'fun': x2},
    # {'type':'eq', 'fun': x3}
]
    
    risk_prem_eq_val = optimize.NonlinearConstraint(lambda x: constraint_risk_prem(x,target_risk_prem), 0, 0)
    result = scipy.optimize.minimize(objective_function, changing_wts, method='SLSQP', constraints=cons, bounds=bounds,  tol=1e-6, options={'maxiter': 1000})
    x = result.x
    full_x = [x[0],x[1], x[2], 1-x[0]-x[1]-x[2]]
    changing_wts = result.x
    print("min sd:", result.fun, full_x)
   

    risk_prem = np.array(full_x) @ np.array([[return_dist[r][0]] for r in return_dist.keys()])
    print(risk_prem.item())

