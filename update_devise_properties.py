from qiskit.providers.models import BackendProperties
from qiskit import IBMQ
import types
# from datetime import datetime 
from dateutil.tz import tzutc
from qiskit.transpiler import PassManager
from qiskit.compiler import transpile
from qiskit import QuantumCircuit
from qiskit import QiskitError, execute, BasicAer
from collections import Iterable  
from qiskit.tools.visualization import plot_histogram
# from qiskit.providers.models import BackendProperties
# from qiskit.providers.models.backendproperties import Nduv, Gate
import random                         


def flatten(items):
    """Yield items from any nested iterable; see Reference."""
    for x in items:
        if isinstance(x, Iterable) and not isinstance(x, (str, bytes)):
            for sub_x in flatten(x):
                yield sub_x
        else:
            yield x

#backend configuration
IBMQ.save_account('53d53f699d4b706ce125b3fea389764d22ca4a5e031581e0db1e13abaa8a565b1ec61e5b9f3ddeaf507b912aff0e1229b38ad38783ecc072df17686610e7b00d', overwrite=True)
IBMQ.update_account()
IBMQ.load_account()

# devise_hash_sunday = {}
devise_hash_monday = {}
# devises = ['ibmq_vigo', 'ibmq_ourense', 'ibmq_16_melbourne', 'ibmqx2']
devises = ['ibmq_vigo', 'ibmqx2']
# devises = ['ibmq_16_melbourne']
for devise_name in devises:
  # for i in range(10):
  for i in range(10):
    devise = IBMQ.get_backend(devise_name)
    name = str(devise.name())
    devise_hash_monday[name] = devise_hash_monday.get(name) or {}
    # properties = devise.properties()
    # coupling_map = devise.configuration().coupling_map
    properties = devise.properties()
    coupling_map = devise.configuration().coupling_map

    #Quantum Circuit
    circ = QuantumCircuit.from_qasm_file("grover_search.qasm")
    # coupling_map = CouplingMap(coupling_list=coupling_map)
    # pm = PassManager()
    circuit=transpile(circ, backend=devise, coupling_map= coupling_map, backend_properties=properties)
    # %matplotlib inline
    # circuit.draw(output='mpl')
    # backend = Aer.get_backend('qasm_simulator')
    backend = devise
    result = execute(circuit, backend=backend, shots = 1024).result()
    count = result.get_counts()
    # plot_histogram(count)
    devise_hash_monday[name]['original_result'] = count

    test_properties = properties.to_dict()

    # devise_hash_monday[name]['properties'] = test_properties


    #Noise constraints changed
    parsed_properties =  test_properties.copy()
    qubits = [[y['value'] for y in x] for x in parsed_properties['qubits']]
    qubits_errors = list(set(flatten(qubits)))
    gates_errors = list(set([ x['parameters'][0]['value'] for x in parsed_properties['gates']]))

    gates_hash_list = []
    for gate in parsed_properties['gates']:
      gates_hash = {}
      for k in gate:
        lists = []
        if k == 'parameters':
          first_element = gate[k][0]
          data = [x for x in gates_errors if x != first_element['value']]
          random_data = random.choice(data)
          first_element['value'] = random_data
          gates_hash[k] = [first_element]
        else:
          gates_hash[k] = gate[k]
      gates_hash_list.append(gates_hash)

    qubit_list = []
    for grouped_qubit in parsed_properties['qubits']:
      data = []
      for qubit in grouped_qubit:
        data_hash = qubit
        data_hash['value'] = random.choice([x for x in qubits_errors if x != data_hash['value']])
        data.append(data_hash)
      qubit_list.append(data)

    parsed_properties['gates'] = gates_hash_list
    parsed_properties['qubits'] = qubit_list
      
    new_properties = BackendProperties.from_dict(parsed_properties)
    new_circuit=transpile(circ, backend=devise, coupling_map= coupling_map, backend_properties=new_properties)
    # %matplotlib inline
    # new_circuit.draw(output='mpl')
    # backend = Aer.get_backend('qasm_simulator')
    key = 'changed_' + str(i)
    devise_hash_monday[name][key] = devise_hash_monday[name].get(key) or {}
    devise_hash_monday[name][key]['properties'] = new_properties.to_dict()
    devise_hash_monday[name][key]['originaLproperties'] = test_properties
    new_result = execute(new_circuit, backend=backend, shots = 1024).result()
    new_counts = result.get_counts()
    devise_hash_monday[name][key]['result'] = new_counts
    # from qiskit.tools.visualization import plot_histogram
    # plot_histogram(new_counts)

