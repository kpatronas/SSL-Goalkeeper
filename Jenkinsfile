node {
 
 def commit_id
 
 stage('Preparation') {
  checkout scm
  sh "git rev-parse --short HEAD > .git/commit-id"
  commit_id = readFile('.git/commit-id').trim()
 }
 
 stage('test') {
  def myTestContainer = docker.build("test-python", "./dockerfiles/test-python")
  myTestContainer.inside {
       sh 'python tests.py'
  }
  myTestContainer.stop()
 }
 
 stage('docker build/push') {            
  docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
   def app = docker.build("kpat/test1:${commit_id}", '.').push()
  }
 }
 
}
