#!/usr/bin/env groovy
pipeline {
    agent any

    environment {
        VALUE_ONE = '1'
        VALUE_TWO = '2'
        VALUE_THREE = '3'
    }
    
    stages {
        stage("Script Execution") {
            when {
                branch 'master'
            }
            steps {
                echo 'Script Execution Started'
                sh 'docker run -it --rm --name downloader -v "$PWD":/usr/src/app -w /usr/src/app python:2 python downloader.py'
            }
        }

        stage("Script Ended") {
            steps {
                echo 'Script Completed'
            }
        }
    }

    post {
        failure {
            // notify users when the Pipeline fails
            mail to: 'team@example.io',
                    subject: "Failed Pipeline: ${currentBuild.fullDisplayName}",
                    body: "Something is wrong with ${env.BUILD_URL}"
        }
    }
}