import numpy as np
import os
import sys
import tensorflow as tf
from PIL import Image


sys.path.append("./models/research")
from object_detection.utils import ops as utils_ops
from object_detection.utils import label_map_util


def load_image_into_numpy_array(image):
  (im_width, im_height) = image.size
  return np.array(image.getdata()).reshape(
      (im_height, im_width, 3)).astype(np.uint8)

def run_inference_for_single_image(image, graph):
  with graph.as_default():
    with tf.Session() as sess:
      # Get handles to input and output tensors
      ops = tf.get_default_graph().get_operations()
      all_tensor_names = {output.name for op in ops for output in op.outputs}
      tensor_dict = {}
      for key in [
          'num_detections', 'detection_boxes', 'detection_scores',
          'detection_classes', 'detection_masks'
      ]:
        tensor_name = key + ':0'
        if tensor_name in all_tensor_names:
          tensor_dict[key] = tf.get_default_graph().get_tensor_by_name(
              tensor_name)
      if 'detection_masks' in tensor_dict:
        # The following processing is only for single image
        detection_boxes = tf.squeeze(tensor_dict['detection_boxes'], [0])
        detection_masks = tf.squeeze(tensor_dict['detection_masks'], [0])
        # Reframe is required to translate mask from box coordinates to image coordinates and fit the image size.
        real_num_detection = tf.cast(tensor_dict['num_detections'][0], tf.int32)
        detection_boxes = tf.slice(detection_boxes, [0, 0], [real_num_detection, -1])
        detection_masks = tf.slice(detection_masks, [0, 0, 0], [real_num_detection, -1, -1])
        detection_masks_reframed = utils_ops.reframe_box_masks_to_image_masks(
            detection_masks, detection_boxes, image.shape[0], image.shape[1])
        detection_masks_reframed = tf.cast(
            tf.greater(detection_masks_reframed, 0.5), tf.uint8)
        # Follow the convention by adding back the batch dimension
        tensor_dict['detection_masks'] = tf.expand_dims(
            detection_masks_reframed, 0)
      image_tensor = tf.get_default_graph().get_tensor_by_name('image_tensor:0')

      # Run inference
      output_dict = sess.run(tensor_dict,
                             feed_dict={image_tensor: np.expand_dims(image, 0)})

      # all outputs are float32 numpy arrays, so convert types as appropriate
      output_dict['num_detections'] = int(output_dict['num_detections'][0])
      output_dict['detection_classes'] = output_dict[
          'detection_classes'][0].astype(np.uint8)
      output_dict['detection_boxes'] = output_dict['detection_boxes'][0]
      output_dict['detection_scores'] = output_dict['detection_scores'][0]
      if 'detection_masks' in output_dict:
        output_dict['detection_masks'] = output_dict['detection_masks'][0]
  return output_dict


def crop_and_save(image_path, save_path, percent_points=0.0):
  MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
  PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'


  PATH_TO_LABELS = os.path.join('.', 'models', 'research', 'object_detection', 'data', 'mscoco_label_map.pbtxt')
  category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')
  

  with Image.open(image_path) as image:
    image_np = load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    output_dict = run_inference_for_single_image(image_np, detection_graph)

    best_box = output_dict["detection_boxes"][0]

    (rawX0, rawY0, rawX1, rawY1) = best_box

    rawX0 -= percent_points
    rawY0 -= percent_points
    rawX1 += percent_points
    rawY1 += percent_points
  
    (width, height) = image.size
    rawX0 *= width
    rawX1 *= width
    rawY0 *= height
    rawY1 *= height

    image.crop( (rawX0, rawY0, rawX1, rawY1) ).save(save_path)


def dart_coords(image_path):
  """
  Returns the coordinates of a dart as an ordered pair
  """

  MODEL_NAME = 'ssd_mobilenet_v1_coco_2017_11_17'
  PATH_TO_FROZEN_GRAPH = MODEL_NAME + '/frozen_inference_graph.pb'


  PATH_TO_LABELS = os.path.join('.', 'models', 'research', 'object_detection', 'data', 'mscoco_label_map.pbtxt')
  category_index = label_map_util.create_category_index_from_labelmap(PATH_TO_LABELS, use_display_name=True)

  detection_graph = tf.Graph()
  with detection_graph.as_default():
    od_graph_def = tf.GraphDef()
    with tf.gfile.GFile(PATH_TO_FROZEN_GRAPH, 'rb') as fid:
      serialized_graph = fid.read()
      od_graph_def.ParseFromString(serialized_graph)
      tf.import_graph_def(od_graph_def, name='')


  with Image.open(image_path) as image:
    image_np = load_image_into_numpy_array(image)
    image_np_expanded = np.expand_dims(image_np, axis=0)
    output_dict = run_inference_for_single_image(image_np, detection_graph)
    
    for (i, identifier) in enumerate( output_dict["detection_classes"] ):
      objectClass = category_index[identifier]["name"]
      if objectClass == "tie":
        box = output_dict["detection_boxes"][i]
        best_box = box
        break
    

    (rawX0, rawY0, rawX1, rawY1) = best_box
    (width, height) = image.size
    rawX0 *= width
    rawX1 *= width
    rawY0 *= height
    rawY1 *= height

    return ( (rawX0+rawX1)/2, (rawY0+rawY1)/2 )



if __name__ == "__main__":
	filePath = "image3darts.png"
	crop_and_save(filePath, "crop_testing.jpg")
	print(dart_coords(filePath))
