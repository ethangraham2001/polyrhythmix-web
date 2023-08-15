import subprocess
import os.path

current_directory = os.path.dirname(os.path.abspath(__file__))
filename = 'poly'
PATH = os.path.join(current_directory, filename)
MIDI_FILEPATH = os.path.join(current_directory, '..', 'midi_files') 

def get_midi_filepath(midi_name: str):
    """
    generates the midi file path for a midi of a given name

    :param midi_name: the name of the `.mid` file
    """
    print(f'midi filepath: {MIDI_FILEPATH}')
    return os.path.join(MIDI_FILEPATH, midi_name+'.mid')

def run_poly_executable(args: list[str], midi_name: str=None):
    """
    runs the `poly` executable file 

    :param args: args to be passed to `poly`
    :param midi_name: the name of the `.mid` file outputted
    """

    if midi_name:
        midi_name = get_midi_filepath(midi_name)
        args.append('-o')
        args.append(midi_name)

    print(f'poly path: {PATH}')
    result = subprocess.run([PATH] + args, capture_output=True, text=True)

    return result.stdout, result.stderr
