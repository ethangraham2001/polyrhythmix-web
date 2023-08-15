from rest_framework import serializers

class PolyrhythmixSerializer(serializers.Serializer):
    """
    Serializes JSON into args for `poly` executable
    """

    kick_activate = serializers.BooleanField(default=True)
    kick_pattern = serializers.CharField(default='32xx16xx')

    snare_activate = serializers.BooleanField(default=True)
    snare_pattern = serializers.CharField(default='4--x-')

    hihat_activate = serializers.BooleanField(default=True)
    hihat_pattern = serializers.CharField(default='8x')

    crash_activate = serializers.BooleanField(default=False)
    crash_pattern = serializers.CharField(default='')