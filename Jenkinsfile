pipeline {
    // 1. Agente: Dónde se ejecutará la pipeline. 'any' significa cualquier agente disponible.
    // Para esta configuración simple, asumimos que Jenkins puede ejecutar Docker y kubectl directamente
    // (requiere montar el docker.sock y que kubectl/minikube estén en el PATH del host o instalados)
    agent any

    // 2. Variables de Entorno Globales para la Pipeline
    environment {
        IMAGE_NAME = 'mi-prediccion-iris'
        // Usamos el número de build de Jenkins para generar etiquetas únicas para las imágenes
        IMAGE_TAG = "v${env.BUILD_NUMBER}"
        KUBERNETES_YAML_DIR = 'kubernetes'
        MODEL_FILE = 'iris_model.joblib'
    }

    // 3. Etapas (Stages) de la Pipeline
    stages {
        // Etapa 1: Obtener el código fuente
        stage('Checkout') {
            steps {
                // Comando integrado de Jenkins para clonar/actualizar el repositorio
                // configurado en el Job de Jenkins.
                checkout scm
                script {
                    // Opcional: Mostrar el commit que se está usando
                    def commitHash = sh(script: 'git rev-parse --short HEAD', returnStdout: true).trim()
                    echo "Pipeline ejecutándose en el commit: ${commitHash}"
                }
            }
        }

        // Etapa 2: Asegurar que el Modelo Exista (o entrenarlo)
        stage('Prepare Model') {
            steps {
                script {
                    // Verificamos si el archivo del modelo existe en el workspace
                    if (!fileExists(env.MODEL_FILE)) {
                        echo "Archivo de modelo ${env.MODEL_FILE} no encontrado."
                        // Asumimos que Python está disponible en el entorno donde corre Jenkins
                        // ¡Esto puede necesitar configuración adicional en un Jenkins real!
                        echo "Ejecutando script de entrenamiento: python scripts/train.py"
                        // 'sh' ejecuta comandos de shell
                        sh 'python3 scripts/train.py'
   
                    } else {
                        echo "Archivo de modelo ${env.MODEL_FILE} encontrado."
                    }
                }
            }
        }

        // Etapa 3: Construir la Imagen Docker
        stage('Build Docker Image') {
            steps {
                echo "Construyendo imagen Docker ${env.IMAGE_NAME}:${env.IMAGE_TAG}..."
                // Usamos el comando 'sh' para ejecutar el build de Docker
                sh "docker build -t ${env.IMAGE_NAME}:${env.IMAGE_TAG} ."
            }
        }

        // Etapa 4: Cargar Imagen en Minikube (Específico para nuestro entorno local)
        stage('Load Image into Minikube') {
            steps {
                echo "Cargando imagen ${env.IMAGE_NAME}:${env.IMAGE_TAG} en Minikube..."
                // Ejecutamos el comando minikube image load
                sh "minikube image load ${env.IMAGE_NAME}:${env.IMAGE_TAG}"
            }
        }

        // Etapa 5: Desplegar en Kubernetes
        stage('Deploy to Kubernetes') {
            steps {
                echo "Desplegando la aplicación en Kubernetes..."
                // IMPORTANTE: Actualizar dinámicamente la etiqueta de la imagen en deployment.yaml
                // Usamos 'sed' para reemplazar la línea 'image:'. Esto es simple pero FRÁGIL.
                // Herramientas como Kustomize o Helm son mejores para esto en producción.
                // sed -i 's|image: .*|image: NUEVA_IMAGEN|g' archivo.yaml
                sh "sed -i 's|image: .*|image: ${env.IMAGE_NAME}:${env.IMAGE_TAG}|g' ${env.KUBERNETES_YAML_DIR}/deployment.yaml"
                echo "deployment.yaml actualizado para usar la imagen ${env.IMAGE_NAME}:${env.IMAGE_TAG}"

                // Aplicar los manifiestos de Kubernetes
                sh "kubectl apply -f ${env.KUBERNETES_YAML_DIR}/deployment.yaml"
                sh "kubectl apply -f ${env.KUBERNETES_YAML_DIR}/service.yaml" // Re-aplicar el servicio por si acaso

                // Opcional: Esperar a que el despliegue termine exitosamente
                echo "Esperando que el despliegue se complete..."
                sh "kubectl rollout status deployment/iris-deployment --timeout=120s"
            }
        }
    } // Fin de stages

    // 4. Acciones Post-Build
    post {
        // 'always' se ejecuta siempre, sin importar el resultado de la pipeline
        always {
            echo 'Limpiando el workspace...'
            // Revertir el cambio hecho por 'sed' en deployment.yaml
            // para que el workspace de Git quede limpio para la próxima ejecución.
            sh "git checkout -- ${env.KUBERNETES_YAML_DIR}/deployment.yaml"
        }
        // Se ejecuta solo si la pipeline fue exitosa
        success {
            echo '¡Pipeline completada exitosamente!'
            // Aquí podrías añadir notificaciones (Email, Slack, etc.)
        }
        // Se ejecuta solo si la pipeline falló
        failure {
            echo '¡La Pipeline falló!'
            // Aquí podrías añadir notificaciones de error
        }
    } // Fin de post
} // Fin de pipeline