pipeline {
  agent any
  tools {
    maven 'Maven'
  }
  stages {
    stage ('Initialize') {
      steps {
        sh '''
          echo "PATH = ${PATH}"
          echo "M2_HOME = ${M2_HOME}"
          '''
      }
    }
    stage ('Build') {
      steps {
      sh 'mvn clean package' 
      }
    }
    stage ('Deploy-to-Tomcat') {
      steps {
        sshagent(['tomcat']) {
          sh 'scp -o StrictHostKeyChecking=no target/*.war ubuntu@13.127.144.150:/prod/apache-tomcat-9.0.63/webapps/webapp.war'
        }
      }
    }
  }
}
