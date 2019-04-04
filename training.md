# Entrenamiento
Para el entrenamiento se utiliza el [Tensorflow Object Detection API](https://github.com/tensorflow/models/tree/master/research/object_detection). Para ello clonamos el repositorio de Tensorflow/Models.
```bash
git clone https://github.com/tensorflow/models.git
```

Usamos el dataset de rostros [WIDERFACE](http://mmlab.ie.cuhk.edu.hk/projects/WIDERFace/). Para el entrenamiento se requieren los datos en forma de TFRecord. Para esta conversión seguimos una parte de un [tutorial](https://towardsdatascience.com/how-to-train-a-tensorflow-face-object-detection-model-3599dcd0c26f), el cual indica el uso de ciertos scripts en Python que se obtienen del [repositorio](https://github.com/qdraw/tensorflow-face-object-detector-tutorial).
```bash
git clone https://github.com/qdraw/tensorflow-face-object-detector-tutorial.git
cd tensorflow-face-object-detector-tutorial/
pip install -r requirements.txt
```
Los siguientes scripts realizan la descarga conversión de los datos a TFRecords.
```bash
python 001_down_data.py
python 002_data-to-pascal-xml.py
python 003_xml-to-csv.py
python 004_generate_tfrecord.py --images_path=data/tf_wider_train/images --csv_input=data/tf_wider_train/train.csv  --output_path=data/train.record
python 004_generate_tfrecord.py --images_path=data/tf_wider_val/images --csv_input=data/tf_wider_val/val.csv  --output_path=data/val.record
```
También se descarga un modelo ssd_mobilenet_v1 entrenado con COCO. Se puede utilizar este modelo o cualquier modelo ssd_mobilenet_v1 que se encuentra dentro del [Tensorflow detection model zoo](https://github.com/tensorflow/models/blob/master/research/object_detection/g3doc/detection_model_zoo.md). Estos modelos están pre-entrenados sin embargo se tienen que entrenar desde cero puesto que el AIY Vision Kit sólo soporta modelos de menor profundidad.

Para acelerar el entrenamiento hacemos uso de un checkpoint de un entrenamiento de 870,894 steps con 20 clases proporcionado por [zhoujustin](https://github.com/zhoujustin) que podemos obtener en este [enlace](https://drive.google.com/file/d/1_MeZ8kvmpNibPZvSJGnwKNRATeuyxNtu/view?usp=sharing).

Configuramos el entrenamiento en un archivo pipeline. Se puede descargar el archivo de este [enlace](https://github.com/tensorflow/models/blob/master/research/object_detection/samples/configs/embedded_ssd_mobilenet_v1_coco.config). Este archivo lo configuramos de acuerdo a nuestras necesidades.
Modificamos el valor de _num\_classes_ a 1 puesto que sólo vamos a detectar una clase, rostros.
```bash
model {
  ssd {
    num_classes: 1
```
Nos aseguramos de que _feature\_extractor_ tenga como _type_ 'embedded\_ssd\_mobilenet\_v1' y configuramos _depth\_multiplier_ con un valor de 0.125 (el soportado por el AIY Vision Kit).
```bash
feature_extractor {
  type: 'embedded_ssd_mobilenet_v1'
  min_depth: 16
  depth_multiplier: 0.125
```
En la parte de _train\_config_ configuramos el checkpoint desde el que se realizará el finetuning del modelo. En este caso usamos el checkpoint previamente descargado de [zhoujustin](https://github.com/zhoujustin).
```bash
fine_tune_checkpoint:"path_a_checkpoint/model.ckpt-870894"
  from_detection_checkpoint: true
```
En _train\_input\_reader_ y _eval\_input\_reader_ se configuran los paths a los TFRecords de entrenamiento y evaluación respectivamente. Ambos utilizan el mismo _label\_map\_path_.
```bash
train_input_reader: {
  tf_record_input_reader {
    input_path: "path_a_datos/data/train.record"
  }
  label_map_path: "path_a_datos/face_label.pbtxt"
}
```
```bash
eval_input_reader: {
  tf_record_input_reader {
    input_path: "path_a_datos/data/val.record"
  }
  label_map_path: "path_a_datos/face_label.pbtxt"
```
Teniendo el archivo pipeline configurado podemos proceder al entrenamiento. Para esto declaramos unas variables de entorno por facilidad.
```bash
PIPELINE_CONFIG_PATH=path/embedded_ssd_mobilenet_v1_coco.config
MODEL_DIR=path_de_salida_
NUM_TRAIN_STEPS=200000
SAMPLE_1_OF_N_EVAL_EXAMPLES=1
```
Y utilizamos el script _model\_main.py_ del Object Detection API.
```bash
python path_a_api/models/research/object_detection/model_main.py \
    --pipeline_config_path=${PIPELINE_CONFIG_PATH} \
    --model_dir=${MODEL_DIR} \
    --num_train_steps=${NUM_TRAIN_STEPS} \
    --sample_1_of_n_eval_examples=$SAMPLE_1_OF_N_EVAL_EXAMPLES \
    --alsologtostderr
```
Con este entrenamiento obtenemos un checkpoint, el cual se usa para exportar el grafo de inferencia del modelo. Para ello también utilizamos un script del API. Y obtenemos un _frozen\_inference\_graph.pb_
```bash
python path_a_api_/models/research/object_detection/export_inference_graph.py \
    --input_type=image_tensor \
    --pipeline_config_path=path_a_pipeline/embedded_ssd_mobilenet_v1_coco.config \
    --trained_checkpoint_prefix=${MODEL_DIR}/model.ckpt-200000 \
    --output_directory=path_de_salida
```
Contando con el grafo de inferencia congelado se tiene que usar el [Bonnet Compiler de Google](https://dl.google.com/dl/aiyprojects/vision/bonnet_model_compiler_latest.tgz) que se indica debe correrse en Linux. Debemos indicar el archivo del grafo, el path de salida, el nombre del tensor de entrada, el nombre del tensor de salida y el tamaño del sensor de entrada.
```bash
./bonnet_model_compiler.par \
    --frozen_graph_path=path_a_grafo/frozen_inference_graph.pb \
    --output_graph_path=path_de_salida/frozen_inference_graph.binaryproto \
    --input_tensor_name=“Preprocessor/sub” \
    --output_tensor_names=“concat,concat1” \
    --input_tensor_size=256 \
```
El archivo de salida _frozen\_inference\_graph.binaryproto_ es el que se debe enviar al AIY Vision Kit para utilizarse. Esto puede realizarse mediante SSH teniendo la IP del Vision Kit conectado a una red.
```bash
scp path_a_binaryproto/frozen_inference_graph.binaryproto pi@[ip del vision kit]:/home/pi/
```
