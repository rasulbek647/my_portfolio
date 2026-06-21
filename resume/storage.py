"""
Custom Cloudinary storage backends.
PDF va boshqa xom fayllar uchun RawMediaCloudinaryStorage ishlatiladi,
bu esa ularni 'image/upload' emas, 'raw/upload' yo'li orqali yuklaydi
va brauzer to'g'ri ochishi mumkin bo'ladi.
"""
import os

try:
    from cloudinary_storage.storage import RawMediaCloudinaryStorage as _Raw
    from django.core.files.storage import FileSystemStorage as _FS

    class PDFCloudinaryStorage(_Raw):
        """
        PDF va boshqa hujjatlarni Cloudinary'ga raw/upload sifatida yuklaydi.
        Bu brauzerga to'g'ri Content-Type qaytaradi va PDF ko'rsatiladi.
        """
        pass

except ImportError:
    # Cloudinary o'rnatilmagan bo'lsa (local dev), oddiy storage ishlatiladi
    from django.core.files.storage import FileSystemStorage as PDFCloudinaryStorage  # noqa
