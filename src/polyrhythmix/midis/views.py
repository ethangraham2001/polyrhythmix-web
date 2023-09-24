import random, string, os

from django.shortcuts import render
from django.utils.termcolors import colorize
from django.http import HttpResponse
from django.utils.http import quote

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status

from .serializers import PolyrhythmixSerializer

from executables.execute import run_poly_executable, get_midi_filepath

class GenerateMidiView(APIView):
    """
    Generates a midi file from JSON request
    """
    def generate_short_uid(self):
        """
        Generates an 8-digit-uid
        """

        LENGTH = 12 
        chars = string.ascii_letters + string.digits 
        return ''.join(random.choice(chars) for _ in range(LENGTH))

    def post(self, request):
        serializer = PolyrhythmixSerializer(data=request.data)

        if not serializer.is_valid():
            print(colorize('[SERIALIZER ERROR]', fg='red'))
            return Response(
                {
                    'message': 'Failure: invalid data'
                },
                status=status.HTTP_400_BAD_REQUEST
            )
        print(colorize('[SERIALIZER OK]', fg='green'))


        poly_args = []
        data = serializer.data
        instruments = {
            'kick': '--kick',
            'snare': '--snare',
            'hihat' : '--hi-hat',
            'crash' : '--crash',
        }

        # kind of voodoo. Iterate over serializer data and add it to args 
        for instrument in instruments:
            is_active = serializer.data.get(instrument + '_activate')
            if is_active: 
                poly_args.append(instruments[instrument])
                poly_args.append(data[instrument + '_pattern'])

        midi_name = self.generate_short_uid()
        poly_stdout, poly_stderr = run_poly_executable(poly_args, 
                                                       midi_name=midi_name)

        print(colorize(f"Generating: {poly_args}", fg='blue', opts=['bold']))
        print(colorize(poly_stdout, fg='cyan'))
        print(colorize(poly_stderr, fg='red'))

        poly_stdout = poly_stdout.split()

        return Response(
            {
                'message': 'Success!',
                'convergence_bars': poly_stdout[2],
                'file_name': midi_name
            },
            status=status.HTTP_200_OK
        )


class DownloadMidiView(APIView):
    """
    Handles the downloading of midi files
    """

    def get(self, request, midi_name):
        
        midi_filepath = get_midi_filepath(midi_name=midi_name)
        print(colorize(f'path: {midi_filepath}', fg='blue'))

        with open(midi_filepath, 'rb') as midi_file:
            midi_content = midi_file.read()

        
        midi_name += '.mid'
        print(midi_name)
        response = HttpResponse(midi_content, content_type='audio/x-midi')
        response['Content-Disposition'] = f'attachment; "filename={quote(midi_name)}"'

        return response
