import Robot from '../robot'
import Device from '../device'

export default interface DatabaseInterface {
  getAllRobots(): Array<Robot>;
  getAllDevices(): Array<Device>;
  findRobotByUuid(uuid: string): Robot;
  saveRobot(robot: Robot): boolean;
  removeRobot(socketId: string): boolean;
  saveDevice(device: Device): boolean;
  getAllDevicesByRobotUuid(uuid: string): Array<Device>;
  updateRobotRosnodes(uuid: string, rosnodes: Array<string>): boolean;
}
