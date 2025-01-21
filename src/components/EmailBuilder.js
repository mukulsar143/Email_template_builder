import React, { useState, useEffect } from "react";
import axios from "axios";

const EmailBuilder = () => {
  const [title, setTitle] = useState("");
  const [content, setContent] = useState("");
  const [footer, setFooter] = useState("");
  const [imageUrl, setImageUrl] = useState("");
  const [emailLayout, setEmailLayout] = useState("");
  const [isSaving, setIsSaving] = useState(false);
  const [isUploading, setIsUploading] = useState(false);

  useEffect(() => {
    axios
      .post("http://127.0.0.1:8000/api/getEmailLayout/", {
        title,
        content,
        footer,
        image_url: imageUrl,
      })
      .then((response) => {
        setEmailLayout(response.data.rendered_layout);
      });
  }, [title, content, footer, imageUrl]);

  const handleImageUpload = (event) => {
    const file = event.target.files[0];
    if (!file) return;

    const formData = new FormData();
    formData.append("image", file);
    setIsUploading(true);

    axios
      .post("http://127.0.0.1:8000/api/uploadImage/", formData)
      .then((response) => {
        const uploadedImageUrl = response.data.image_url.trim();
        if (uploadedImageUrl.startsWith("http://") || uploadedImageUrl.startsWith("https://")) {
          setImageUrl(uploadedImageUrl);
        } else {
          alert("Invalid image URL received from the server.");
        }
      })
      .catch((error) => console.error("Error uploading image", error))
      .finally(() => setIsUploading(false));
  };

  const handleSaveConfig = () => {
    const emailConfig = {
      title: title.trim(),
      content: content.trim(),
      footer: footer.trim(),
      image_url: imageUrl || null,
    };

    setIsSaving(true);

    axios
      .post("http://127.0.0.1:8000/api/uploadEmailConfig/", emailConfig)
      .then(() => {
        alert("Email template saved successfully!");
      })
      .catch((error) => console.error("Error saving email config:", error))
      .finally(() => setIsSaving(false));
  };

  const handleRenderTemplate = () => {
    const emailConfig = { title, content, footer, image_url: imageUrl };

    axios
      .post("http://127.0.0.1:8000/api/renderAndDownloadTemplate/", emailConfig)
      .then((response) => {
        const link = document.createElement("a");
        link.href = "data:text/html;charset=utf-8," + encodeURIComponent(response.data.rendered_html);
        link.download = "email_template.html";
        link.click();
      })
      .catch((error) => console.error("Error rendering template:", error));
  };

  return (
    <div className="min-h-screen bg-gray-50 flex flex-col items-center py-10">
      <div className="w-full max-w-5xl bg-white shadow-lg rounded-lg p-8">
        <h1 className="text-4xl font-bold text-gray-800 text-center mb-8">
          Email Template Builder
        </h1>
        <div className="space-y-6">
          <div>
            <label className="block text-lg font-semibold text-gray-700">Email Title</label>
            <input
              type="text"
              value={title}
              onChange={(e) => setTitle(e.target.value)}
              placeholder="Enter email title"
              className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:ring focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-lg font-semibold text-gray-700">Email Content</label>
            <textarea
              value={content}
              onChange={(e) => setContent(e.target.value)}
              placeholder="Enter email content"
              rows="6"
              className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:ring focus:ring-blue-500 focus:outline-none"
            ></textarea>
          </div>
          <div>
            <label className="block text-lg font-semibold text-gray-700">Email Footer</label>
            <input
              type="text"
              value={footer}
              onChange={(e) => setFooter(e.target.value)}
              placeholder="Enter email footer"
              className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:ring focus:ring-blue-500 focus:outline-none"
            />
          </div>
          <div>
            <label className="block text-lg font-semibold text-gray-700">Upload Image</label>
            <input
              type="file"
              onChange={handleImageUpload}
              className="w-full mt-2 p-3 border border-gray-300 rounded-lg focus:ring focus:ring-blue-500 focus:outline-none"
            />
            {isUploading && <p className="text-blue-500 text-sm mt-2">Uploading image...</p>}
            {imageUrl && (
              <div className="mt-4 flex justify-center">
                <img src={imageUrl} alt="Uploaded preview" className="w-40 h-40 object-cover rounded-lg shadow" />
              </div>
            )}
          </div>
          <div className="flex gap-4">
            <button
              onClick={handleSaveConfig}
              disabled={isSaving}
              className="flex-1 py-3 bg-blue-600 text-white rounded-lg hover:bg-blue-700 disabled:opacity-50"
            >
              {isSaving ? "Saving..." : "Save Template"}
            </button>
            <button
              onClick={handleRenderTemplate}
              className="flex-1 py-3 bg-green-600 text-white rounded-lg hover:bg-green-700"
            >
              Download Template
            </button>
          </div>
        </div>
        <div className="mt-8">
          <h2 className="text-2xl font-semibold text-gray-800 mb-4">Email Preview</h2>
          <div
            className="border border-gray-300 rounded-lg p-4 bg-gray-100 shadow-inner"
            dangerouslySetInnerHTML={{ __html: emailLayout }}
          />
        </div>
      </div>
    </div>
  );
};

export default EmailBuilder;
