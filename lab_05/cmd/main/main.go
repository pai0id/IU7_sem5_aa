package main

import (
	"sync"

	"lab_05/internal/stages"
	"lab_05/internal/stages/extract"
	"lab_05/internal/stages/read"
	"lab_05/internal/stages/write"
	"lab_05/internal/tasks"
)

func main() {
	dsn := "postgres://and:1234@localhost:5433/aa"

	const numTasks = 500
	const fileNameFormat = "./data/%d.txt"

	taskQueue1 := make(chan *tasks.Task, 100)
	taskQueue2 := make(chan *tasks.Task, 100)
	taskQueue3 := make(chan *tasks.Task, 100)
	finQueue := make(chan *tasks.Task, 100)
	var wg sync.WaitGroup

	wg.Add(1)
	go tasks.TaskGenerator(numTasks, fileNameFormat, taskQueue1, &wg, &tasks.TaskContext{Dsn: dsn})

	wg.Add(1)
	go stages.ProcessStage("Stage 1 (Read)", taskQueue1, taskQueue2, &wg, read.ReadFileToString)

	wg.Add(1)
	go stages.ProcessStage("Stage 2 (Extract)", taskQueue2, taskQueue3, &wg, extract.ParseText)

	wg.Add(1)
	go stages.ProcessStage("Stage 3 (Write)", taskQueue3, finQueue, &wg, write.WriteToDb)

	wg.Add(1)
	go tasks.TaskAccumulator(finQueue, &wg)

	wg.Wait()
}
