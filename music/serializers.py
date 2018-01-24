from rest_framework import serializers

from music.models import Track, Album


class TrackSerializer(serializers.ModelSerializer):
    class Meta:
        model = Track
        fields = ('order', 'title', 'duration', 'album')
        read_only_fields = ('album',)


class AlbumSerializer(serializers.ModelSerializer):
    tracks = TrackSerializer(many=True)

    class Meta:
        model = Album
        fields = ('album_name', 'artist', 'tracks')

    def create(self, validated_data):
        tracks_data = validated_data.pop('tracks')
        album = Album.objects.create(**validated_data)
        for track_data in tracks_data:
            Track.objects.create(album=album, **track_data)
        return album
    
    def update(self, instance, validated_data):
		instance.album_name = validated_data.get('album_name', instance.album_name)
		instance.artist = validated_data.get('artist', instance.artist)
		instance.save()

		tracks = validated_data.get('tracks')

		if tracks:
			for track in tracks:
				track_id = track.get('id', None)
				if track_id:
					alb_track = Track.objects.get(id=track_id, album=instance)
					alb_track.album = track.get('album', alb_track.album)
					alb_track.order = track.get('order', alb_track.order)
					alb_track.title = track.get('title', alb_track.title)
					alb_track.duration = track.get('duration', alb_track.duration)

					alb_track.save()
				else:
					Track.objects.create(account=instance, **track)

		return instance
