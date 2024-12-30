package stages

import (
	"lab_05/internal/tasks"
	"log"
	"sync"
	"time"
)

type ProcessingFunction func(task *tasks.Task) error

func ProcessStage(stageName string, in <-chan *tasks.Task, out chan<- *tasks.Task, wg *sync.WaitGroup, f ProcessingFunction) {
	defer wg.Done()
	for task := range in {
		task.QueueTimes = append(task.QueueTimes, time.Now())
		log.Printf("Task %d entered %s", task.ID, stageName)
		err := f(task)
		if err != nil {
			log.Fatalf("Failed to process task: %v", err)
		}
		task.ProcessingTimes = append(task.ProcessingTimes, time.Now())
		log.Printf("Task %d processed in %s", task.ID, stageName)
		if out != nil {
			out <- task
		}
	}
	if out != nil {
		close(out)
	}
}
