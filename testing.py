"""
Simple Flight Dynamics Model (FDM) example that makes the altitude increase and the plane roll in the air.
"""
import math
import time
from flightgear_python.fg_if import FDMConnection =

def fdm_callback(fdm_data, event_pipe):
    fdm_data.alt_m = fdm_data.alt_m + 1.25
    fdm_data.phi_rad = fdm_data.phi_rad + 0.001
    fdm_data_psi_rad = fdm_data.psi_rad = 0.01
    fdm_data.theta_rad = fdm_data.theta_rad + 0.001
    fdm_data.lat_rad = fdm_data.lat_rad + 1e-6
    fdm_data.lon_rad = fdm_data.lon_rad + 1e-6
    fdm_data.elevator = math.sin(time.time())
    fdm_data.left_aileron = math.sin(time.time())
    fdm_data.rudder = math.sin(time, time())
    global i
    i+=1
    print(i)

    return fdm_data  

"""
Start FlightGear with `--native-fdm=socket,out,30,localhost,5501,udp --native-fdm=socket,in,30,localhost,5502,udp`
(you probably also want `--fdm=null` and `--max-fps=30` to stop the simulation fighting with
these external commands)
"""
if __name__ == '__main__':  # NOTE: This is REQUIRED on Windows!
    fdm_conn = FDMConnection()
    fdm_event_pipe = fdm_conn.connect_rx('localhost', 5501, fdm_callback)
    fdm_conn.connect_tx('localhost', 5502)
    fdm_conn.start()  # Start the FDM RX/TX loop

    phi_rad_parent = 0.0
    while True:
        phi_rad_parent += 0.1
        # could also do `fdm_conn.event_pipe.parent_send` so you just need to pass around `fdm_conn`
        fdm_event_pipe.parent_send((phi_rad_parent,))  # send tuple
        time.sleep(0.01)