from .views import CanvasView, GalleryView, ImageAPIView

routes = [
    ('/', CanvasView),
    ('/{image_id}', CanvasView),
    ('/image/', ImageAPIView),
    ('/image/{image_id}', ImageAPIView),
    ('/gallery/', GalleryView),
    ('/gallery/{image_id}', GalleryView),
]
