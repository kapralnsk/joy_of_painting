from .views import CanvasView, GalleryView

routes = [
    ('/', CanvasView),
    ('/gallery/', GalleryView),
    ('/gallery/{image_id}', GalleryView),
]
