pipeline {

    agent any

    environment{
        DOCKERHUB_CREDENTIALS=credentials('jo_ashraf')
    }

    stages {

        stage('CI') {
            steps {
               sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u youssefashraf18 --password-stdin"
               sh "pwd"
               sh "ls"
               sh "docker build -f Dockerfile -t amrmahmoud377/backend ."
               sh "docker push amrmahmoud377/backend"
            }
        }

        stage('CD') {
            steps {
               sh "echo ${DOCKERHUB_CREDENTIALS_PSW} | docker login -u youssefashraf18 --password-stdin"
               sh "docker run -d --name backendjenk -p 8000:8000 amrmhamoud377/backend"
            }
        }
    }
}
