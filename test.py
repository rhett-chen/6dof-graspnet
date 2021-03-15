from options.test_options import TestOptions
from data import DataLoader
from models import create_model
from utils.writer import Writer


# this test file is partial test, either sampling network or the evaluator
# for evaluator test, the inputs are grasps annotated in dataset, not generated from sampling network
def run_test(epoch=-1, name="evaluator_pretrained"):
    print('Running Test')
    opt = TestOptions().parse()
    opt.serial_batches = True  # no shuffle
    opt.name = name  # checkpoint dir name, evaluator/gan/vae_pretrained
    dataset = DataLoader(opt)
    model = create_model(opt)
    writer = Writer(opt)
    # test
    writer.reset_counter()

    for i, data in enumerate(dataset):
        model.set_input(data)
        ncorrect, nexamples = model.test()
        writer.update_counter(ncorrect, nexamples)
    writer.print_acc(epoch, writer.acc)
    return writer.acc


if __name__ == '__main__':
    run_test()
