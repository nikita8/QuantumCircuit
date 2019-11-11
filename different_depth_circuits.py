from qiskit.providers.models import BackendProperties
from qiskit import IBMQ
import types
from dateutil.tz import tzutc
from qiskit.compiler import transpile
from qiskit import QuantumCircuit
from qiskit import QiskitError, execute, BasicAer 
from qiskit.tools.visualization import plot_histogram, plot_gate_map, plot_circuit_layout
import random   
from datetime import date                  
from qiskit.tools.monitor import job_monitor
import matplotlib.pyplot as plt
import numpy as np
# %matplotlib inline
import helper_methods as hm

# plot_gate_map(devise, plot_directed=True)

class ValidateQuantumCircuit:
  def __init__(self, devise_name, qasm_file):
    self.devise_name = devise_name
    self.qasm_file = qasm_file
    self.devise = self.load_devise(devise_name)

  def load_devise(self, devise_name):
    IBMQ.save_account('53d53f699d4b706ce125b3fea389764d22ca4a5e031581e0db1e13abaa8a565b1ec61e5b9f3ddeaf507b912aff0e1229b38ad38783ecc072df17686610e7b00d', overwrite=True)
    IBMQ.update_account()
    IBMQ.load_account()
    return IBMQ.get_backend(devise_name)

  def transpile_and_execute_circuits(self, shots=1024, circuit_iteration=1, initial_layout=None, execute_circuits=False):
    circ = QuantumCircuit.from_qasm_file(self.qasm_file)
    transpiled_circuits=transpile([circ]*circuit_iteration, backend=self.devise, optimization_level=1, initial_layout=initial_layout)
    if type(transpiled_circuits) != list:
      transpiled_circuits = [transpiled_circuits]
    depths = [circuit.depth() for circuit in transpiled_circuits]
    circuits = []
    exec_results = []
    for depth in hm.unique(depths):
      index = depths.index(depth)
      circuits.append(transpiled_circuits[index])
    for circuit in circuits:
      hm.show_figure(circuit.draw(output='mpl'))
      if execute_circuits:
        result = execute(circuit, backend=self.devise, shots=shots).result()
        count = result.get_counts()
        exec_results.append({ str(circuit.depth()) : count})
        hm.show_figure(plot_histogram(count, title=str(circuit.depth())))
