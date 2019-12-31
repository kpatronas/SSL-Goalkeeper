node {
 
 def commit_id
 
 stage('Preparation') {
  checkout scm
  sh "git rev-parse --short HEAD > .git/commit-id"
  commit_id = readFile('.git/commit-id').trim()
 }
 
 stage('test') {
  def myTestContainer = docker.build("test-python", "--no-cache -f ./dockerfiles/Dockerfile .")
  myTestContainer.inside {
   sh 'python ./tests/python_tests.py'
  }
 }
 
 stage('push to docker registry') {
  docker.withRegistry('https://index.docker.io/v1/', 'dockerhub') {
   def app = docker.build("kpat/python-pipeline-demo:${commit_id}", "--no-cache -f ./dockerfiles/Dockerfile .").push()
  }
 }       
 
}
