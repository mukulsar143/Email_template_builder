from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from rest_framework import status
from django.template import Template, Context
from django.conf import settings
import os
from .models import EmailTemplate
from .serializers import EmailTemplateSerializer

class GetEmailLayoutView(APIView):
    def post(self, request):
        title = request.data.get("title", "Default Title")
        content = request.data.get("content", "Default Content")
        footer = request.data.get("footer", "Default Footer")
        image_url = request.data.get("image_url", None)

        layout = """<div class="email-container">
            <h1>{{ title }}</h1>
            <p>{{ content }}</p>
            <footer>{{ footer }}</footer>
            {% if image_url %}
                <img src="{{ image_url }}" />
            {% endif %}
        </div>"""

        template = Template(layout)
        context = Context({
            "title": title,
            "content": content,
            "footer": footer,
            "image_url": image_url
        })
        rendered_layout = template.render(context)

        return Response({"rendered_layout": rendered_layout})

class UploadImageView(APIView):
    def post(self, request):
        if "image" not in request.FILES:
            return Response({"detail": "No file provided."}, status=status.HTTP_400_BAD_REQUEST)

        image = request.FILES["image"]
        upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_images")
        os.makedirs(upload_dir, exist_ok=True)

        file_path = os.path.join(upload_dir, image.name)
        with open(file_path, "wb+") as destination:
            for chunk in image.chunks():
                destination.write(chunk)

        # Ensure the URL is fully qualified
        image_url = f"{settings.SITE_URL}{settings.MEDIA_URL}uploaded_images/{image.name}"
        return Response({"image_url": image_url}, status=status.HTTP_201_CREATED)


class UploadEmailConfigView(APIView):
    def post(self, request):
        """
        Handle the POST request to upload email configurations with validation for the `image_url` field.
        """

        image_url = None
        if 'image' in request.FILES:
            image = request.FILES['image']
            upload_dir = os.path.join(settings.MEDIA_ROOT, "uploaded_images")
            os.makedirs(upload_dir, exist_ok=True)

            file_path = os.path.join(upload_dir, image.name)
            with open(file_path, "wb+") as destination:
                for chunk in image.chunks():
                    destination.write(chunk)

            image_url = f"{settings.SITE_URL}{settings.MEDIA_URL}uploaded_images/{image.name}"

        request.data['image_url'] = image_url

        serializer = EmailTemplateSerializer(data=request.data)
        if serializer.is_valid():
            email_config = serializer.save()
            
            print("Saved email config:", email_config)
            
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        
        print("Validation errors:", serializer.errors)
        
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RenderAndDownloadTemplateView(APIView):
    def post(self, request):
        title = request.data.get("title", "Default Title")
        content = request.data.get("content", "Default Content")
        footer = request.data.get("footer", "Default Footer")
        image_url = request.data.get("image_url", None)

        layout = """<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Email Template</title>
    <style>
        body {
            margin: 0;
            padding: 0;
            font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
            background-color: #f3f4f6;
            color: #333;
        }
        .email-container {
            max-width: 700px;
            margin: 30px auto;
            background: #ffffff;
            border-radius: 12px;
            box-shadow: 0 6px 18px rgba(0, 0, 0, 0.1);
            overflow: hidden;
        }
        .header {
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            padding: 30px 20px;
            text-align: center;
        }
        .header h1 {
            margin: 0;
            font-size: 32px;
            font-weight: bold;
            letter-spacing: 1px;
        }
        .content {
            padding: 25px 20px;
            line-height: 1.8;
            font-size: 16px;
        }
        .content p {
            margin: 0 0 15px;
        }
        .content strong {
            color: #6a11cb;
        }
        .image-container {
            text-align: center;
            padding: 20px;
            background-color: #f9f9f9;
        }
        .image-container img {
            max-width: 90%;
            height: auto;
            border-radius: 10px;
            box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
        }
        .cta-button {
            display: inline-block;
            margin: 20px auto;
            padding: 12px 25px;
            background: linear-gradient(135deg, #6a11cb, #2575fc);
            color: white;
            text-decoration: none;
            font-weight: bold;
            border-radius: 30px;
            box-shadow: 0 4px 12px rgba(0, 0, 0, 0.2);
            transition: background 0.3s ease;
        }
        .cta-button:hover {
            background: linear-gradient(135deg, #2575fc, #6a11cb);
        }
        .footer {
            background: #f1f5f9;
            padding: 15px 20px;
            text-align: center;
            border-top: 1px solid #e2e8f0;
            font-size: 14px;
            color: #606f7b;
        }
        .footer a {
            color: #6a11cb;
            text-decoration: none;
            font-weight: bold;
        }
        .footer a:hover {
            text-decoration: underline;
        }
    </style>
</head>
<body>
    <div class="email-container">
        <div class="header">
            <h1>{{ title }}</h1>
        </div>
        <div class="content">
            <p>{{ content }}</p>
        </div>
        {% if image_url %}
        <div class="image-container">
            <img src="{{ image_url }}" alt="Email Image" />
        </div>
        {% endif %}
        <div class="footer">
            <p>{{ footer }}</p>
            <p>Need help? Visit our <a href="#">Support Center</a> or <a href="#">Contact Us</a>.</p>
        </div>
    </div>
</body>
</html>
"""

        template = Template(layout)
        context = Context({
            "title": title,
            "content": content,
            "footer": footer,
            "image_url": image_url
        })
        rendered_html = template.render(context)

        return Response({"rendered_html": rendered_html})
