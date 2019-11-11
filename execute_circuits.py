from different_depth_circuits import ValidateQuantumCircuit
import os
from qiskit.tools.visualization import plot_histogram, plot_gate_map, plot_circuit_layout

# devises = ['ibmq_vigo', 'ibmq_ourense', 'ibmq_16_melbourne', 'ibmqx2']

devise_name = 'ibmq_vigo'
base_path = os.path.realpath('../QasmFiles/')
qasm_file = base_path + '/bv4_circuit.qasm'
quantum_circuit = ValidateQuantumCircuit(devise_name, qasm_file)
plot_gate_map(quantum_circuit.devise, plot_directed=True)
# min depth circuit
quantum_circuit.transpile_and_execute_circuits(circuit_iteration=100, initial_layout=[0,2,3,1,4], execute_circuits=True)
quantum_circuit.transpile_and_execute_circuits(circuit_iteration=100, execute_circuits=True)
#has 2 possibilities
quantum_circuit.transpile_and_execute_circuits(circuit_iteration=100, initial_layout=[4,1,2,3,0], execute_circuits=True)
