package tasks

import (
	"fmt"
	"log"
	"sync"
	"time"
)

type Ingredient struct {
	Name     string `json:"name"`
	Unit     string `json:"unit"`
	Quantity string `json:"quantity"`
}

type Data struct {
	Id          int          `db:"id"`
	Url         string       `db:"url"`
	Title       string       `db:"title"`
	Ingredients []Ingredient `db:"ingredients"`
	Steps       []string     `db:"steps"`
	ImageUrl    string       `db:"image_url"`
}

type TaskContext struct {
	Dsn string
}

type Task struct {
	ID              int
	FileName        string
	Text            string
	Data            Data
	CreationTime    time.Time
	QueueTimes      []time.Time
	ProcessingTimes []time.Time
	CompletionTime  time.Time
	Context         *TaskContext
}

func TaskGenerator(numTasks int, fileNameFormat string, out chan<- *Task, wg *sync.WaitGroup, ctx *TaskContext) {
	defer wg.Done()
	for i := 1; i <= numTasks; i++ {
		task := &Task{
			ID:           i,
			FileName:     fmt.Sprintf(fileNameFormat, i),
			CreationTime: time.Now(),
			Context:      ctx,
		}
		task.QueueTimes = append(task.QueueTimes, time.Now())
		log.Printf("Task %d created: %s", task.ID, task.FileName)
		out <- task
	}
	close(out)
}

func TaskAccumulator(in <-chan *Task, wg *sync.WaitGroup) {
	defer wg.Done()
	var totalLifeTime, totalQueueTime1, totalQueueTime2, totalQueueTime3, totalProcessingTime1, totalProcessingTime2, totalProcessingTime3 time.Duration
	var count int

	for task := range in {
		task.CompletionTime = time.Now()
		lifetime := task.CompletionTime.Sub(task.CreationTime)
		totalLifeTime += lifetime

		totalQueueTime1 += task.QueueTimes[1].Sub(task.QueueTimes[0])
		totalQueueTime2 += task.QueueTimes[2].Sub(task.QueueTimes[1])
		totalQueueTime3 += task.QueueTimes[3].Sub(task.QueueTimes[2])

		totalProcessingTime1 += task.ProcessingTimes[0].Sub(task.QueueTimes[1])
		totalProcessingTime2 += task.ProcessingTimes[1].Sub(task.QueueTimes[2])
		totalProcessingTime3 += task.ProcessingTimes[2].Sub(task.QueueTimes[3])

		count++
		log.Printf("Task %d completed. Lifetime: %v", task.ID, lifetime)
	}

	log.Printf("Average task lifetime: %v", totalLifeTime/time.Duration(count))
	log.Printf("Average queue time for Stage 1: %v", totalQueueTime1/time.Duration(count))
	log.Printf("Average queue time for Stage 2: %v", totalQueueTime2/time.Duration(count))
	log.Printf("Average queue time for Stage 3: %v", totalQueueTime3/time.Duration(count))
	log.Printf("Average processing time for Stage 1: %v", totalProcessingTime1/time.Duration(count))
	log.Printf("Average processing time for Stage 2: %v", totalProcessingTime2/time.Duration(count))
	log.Printf("Average processing time for Stage 3: %v", totalProcessingTime3/time.Duration(count))
}
