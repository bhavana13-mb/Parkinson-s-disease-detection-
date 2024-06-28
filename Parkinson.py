manage.py:
def main():
"""Run administrative tasks.""" os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'finalyear_project.settings') try:
from django.core.management import execute_from_command_line except ImportError as exc:
raise ImportError(
"Couldn't import Django. Are you sure it's installed and "
"available on your PYTHONPATH environment variable? Did you " "forget to activate a virtual environment?"
) from exc execute_from_command_line(sys.argv)


if _name_ == '_main_': main()

views.py:
def upload_image(request):
if request.method == 'POST' and 'image' in request.FILES: # Handle uploaded image
uploaded_image = request.FILES['image'] fs = FileSystemStorage()
filename = fs.save(uploaded_image.name, uploaded_image) uploaded_file_url = fs.url(filename)

# Load the TensorFlow model
model = tf.keras.models.load_model('model/parkinson/spiral_model.h5')


# Load the test image
test_img = cv2.imread('.' + uploaded_file_url) # Adjust the path as necessary if test_img is not None:
# Resize the image to match the model's input shape test_img = cv2.resize(test_img, (256, 256))

# Convert the image to a numpy array and reshape it to add a batch dimension test_input = np.expand_dims(test_img, axis=0)

# Make a prediction on the test image prediction = model.predict(test_input)

# Print the prediction print(prediction)

# Print the predicted class
predicted_class = "Parkinson" if prediction[0][0] >= 0.5 else "Healthy" return render(request, 'result_parkinson.html', {
'uploaded_file_url': uploaded_file_url, 'prediction': predicted_class
})
return render(request, 'upload_p.html')

from django.http import JsonResponse def detect_parkinsons(request):
# Parse user's input data
user_data = request.POST # Assuming POST request with form data


# Assign scores to each symptom based on user's answers vata_scores = [int(user_data.get(f'vata_{i}', 0)) for i in range(1, 19)] pitta_scores = [int(user_data.get(f'pitta_{i}', 0)) for i in range(1, 19)]
kapha_scores = [int(user_data.get(f'kapha_{i}', 0)) for i in range(1, 19)]



# Calculate total score for each dosha total_vata_score = sum(vata_scores) total_pitta_score = sum(pitta_scores) total_kapha_score = sum(kapha_scores)

# Determine likelihood of Parkinson's based on scores
if total_vata_score >= 20 or total_pitta_score >= 20 or total_kapha_score >= 20:
result = "High likelihood of Parkinson's disease. Contact: Dr. Murali Mohan. S MBBS, DNB -

Neurosurgery : 9876543210"
elif total_vata_score >= 15 or total_pitta_score >= 15 or total_kapha_score >= 15: result = "Moderate likelihood of Parkinson's disease."
else:
result = "Low likelihood of Parkinson's disease."


# Return the result
return JsonResponse({'result': result})


from django.shortcuts import render import matplotlib.pyplot as plt
from django.shortcuts import render import matplotlib.pyplot as plt

def parkinson_detection(request): if request.method == 'POST':
# Get values from POST data
vata_values = [int(request.POST.get(f'vata_{i}', 0)) for i in range(1, 30)] pitta_values = [int(request.POST.get(f'pitta_{i}', 0)) for i in range(1, 30)] kapha_values = [int(request.POST.get(f'kapha_{i}', 0)) for i in range(1, 30)]

# Calculate scores

vata_score = sum(vata_values) pitta_score = sum(pitta_values) kapha_score = sum(kapha_values)

# Determine total score
total_score = vata_score + pitta_score + kapha_score


# Determine likelihood of Parkinson's disease threshold_value = 40 # Define your threshold value here if total_score >= threshold_value:
prediction = "Parkinson's disease detected." else:
prediction = "No Parkinson's disease detected."


# Visualization

labels = ['Vata', 'Pitta', 'Kapha']
scores = [vata_score, pitta_score, kapha_score] plt.figure(figsize=(10, 6))
plt.bar(labels, scores, color=['blue', 'orange', 'green']) plt.xlabel('Dosha')
plt.ylabel('Score')
plt.title('Scores of Vata, Pitta, and Kapha')
image_path = 'static/img/scores_bar_chart.png' # Define the image path plt.savefig(image_path) # Save the plot as an image
plt.close()


# Pass prediction result and image path to the template along with total scores return render(request, 'result_p.html', {'prediction': prediction,
'vata_score': vata_score, 'pitta_score': pitta_score, 'kapha_score': kapha_score, 'total_score': total_score, 'image_path': image_path})
else:
return render(request, 'vpk_main.html')


def upload_image_mod(request):
return render(request, 'parkinson_predict.html') urlpatterns = [
path('upload/', views.upload_image, name='upload_image'), path('upload_image_mod/', views.upload_image_mod, name='upload_image_mod'), path('parkinson_detection/', views.parkinson_detection, name='parkinson_detection'),
]
urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)







